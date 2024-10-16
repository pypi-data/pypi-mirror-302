import numpy as np
import pandas as pd
from scipy.stats import ranksums

def MDIC3(G,E):
    T = np.dot(G, E)   # Compute the dot product or matrix multiplication between two arrays.
    #print('T:\n',T)
    Tp = np.linalg.pinv(T)  # Compute the pseudoinverse of a matrix.
    #print('Tp:\n', Tp)
    M = np.dot(Tp, E)
    #print('M:\n', M)

    return M

def filter_CCC_matrix(matrix: np.ndarray, t: float, output_file: str):
    """
    Parameters:
    - matrix: Input 2D NumPy matrix
    - t: Threshold, where the element representing the top-t proportion by absolute value is set to 1
    - output_file: Path of the output CSV file

    Returns:
    - The processed matrix as a DataFrame
    """

    abs_matrix = np.abs(matrix)

    # Flatten the matrix and calculate the number of top-t elements based on absolute values
    flattened = abs_matrix.flatten()
    n_elements = len(flattened)
    top_t_percent_index = int(n_elements * t)

    # Sort the flattened matrix in descending order and get the indices of the top t% largest elements
    sorted_indices = np.argsort(flattened)[::-1]  # Sort in descending order
    top_indices = sorted_indices[:top_t_percent_index]

    # Create a new matrix with zeros
    new_matrix = np.zeros_like(abs_matrix)

    # Set the top t% largest elements to 1
    np.put(new_matrix, top_indices, 1)

    # Set the diagonal elements to 0
    np.fill_diagonal(new_matrix, 0)

    # Convert the matrix to a DataFrame and assign row and column indices
    row_index = np.arange(1, new_matrix.shape[0] + 1)
    col_index = np.arange(1, new_matrix.shape[1] + 1)
    new_matrix_df = pd.DataFrame(new_matrix, index=row_index, columns=col_index)

    # Save the processed matrix to the specified CSV file
    new_matrix_df.to_csv(output_file)

    return new_matrix_df

def process_cell_communication(df: pd.DataFrame, df_labels: pd.DataFrame) -> pd.DataFrame:
    """
    Process cell communication data, calculate communication pairs, and merge label information.

    Parameters:
    - df: DataFrame, cell communication matrix with values 0 or 1
    - df_labels: DataFrame, contains cell label information, must include 'index' and 'label' columns

    Returns:
    - merged_df: DataFrame, contains cell communication pairs and their corresponding labels
    """
    # Calculate the number of elements with a value of 1
    count_1 = df[df == 1].count().sum()
    print('Number of elements with a value of 1:', count_1)

    # Find the row and column indices of elements with a value of 1
    indices_1 = df[df == 1].stack().reset_index()
    indices_1.columns = ['Row', 'Column', 'Communication']

    # Print the number of rows (i.e., the number of communication pairs)
    num_rows = indices_1.shape[0]
    #print("Number of rows:", num_rows)


    # Convert 'Row' and 'Column' to integer type to ensure consistency for merging
    indices_1['Row'] = indices_1['Row'].astype(int)
    indices_1['Column'] = indices_1['Column'].astype(int)
    df_labels['index'] = df_labels['index'].astype(int)


    # Merge with label data to generate the label for the sender cell (label_row)
    merged_df = pd.merge(indices_1, df_labels, left_on='Row', right_on='index')
    merged_df.rename(columns={'label': 'label_row'}, inplace=True)

    # Continue merging to generate the label for the receiver cell (label_column)
    merged_df = pd.merge(merged_df, df_labels, left_on='Column', right_on='index')
    merged_df.rename(columns={'label': 'label_column'}, inplace=True)
    print("merged_df\n:", merged_df)

    # Return the merged result, keeping only the necessary columns
    return merged_df[['Row', 'Column', 'label_row', 'label_column']]

def CellType_Count(label_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the count of each label.

    :param label_df: A DataFrame containing labels, must include a 'label' column.
    :param communication_df: A DataFrame containing communication relationships.
    :return: A DataFrame containing the count of each label, formatted as ['label', 'count'].
    """
    # Calculate the number of occurrences for each label
    label_counts = label_df['label'].value_counts().reset_index()
    label_counts.columns = ['label', 'count']
    return label_counts


def CWCT(label_counts: pd.DataFrame, communication_df: pd.DataFrame) -> pd.DataFrame:
    """
    Populate the communication matrix and calculate the proportion of each element
    based on the product of label counts.

    :param label_counts: A DataFrame containing the count of each label, 'label' column should be the index.
    :param communication_df: A DataFrame containing communication relationships with 'label_row' and 'label_column'.
    :return: A new communication matrix with communication weights between cell types .
    """
    # Ensure 'label' is set as the index in label_counts
    if 'label' in label_counts.columns:
        label_counts.set_index('label', inplace=True)

    # Get unique labels from label_counts and create a zero matrix for communication
    label_indices = label_counts.index.tolist()
    ccc_matrix = pd.DataFrame(0, index=label_indices, columns=label_indices)

    # Populate the communication matrix based on the relationships in communication_df
    for _, row in communication_df.iterrows():
        a = row["label_row"]
        b = row["label_column"]
        if a in ccc_matrix.index and b in ccc_matrix.columns:
            ccc_matrix.at[a, b] += 1

    # Create a new DataFrame to store the calculated communication weights between cell types
    ccc_matrix_new = pd.DataFrame(0.0, index=ccc_matrix.index, columns=ccc_matrix.columns)

    # Calculate the proportion for each element
    for i, row in ccc_matrix.iterrows():
        for j, value in row.items():
            # Get the product of the corresponding count values
            count_product = label_counts.loc[i, 'count'] * label_counts.loc[j, 'count']
            # Compute the new value
            new_value = value / count_product if count_product != 0 else 0.0
            ccc_matrix_new.loc[i, j] = new_value

    return ccc_matrix_new

def Rank_sum_test(expression_data: pd.DataFrame, cell_types: pd.DataFrame, p_value_threshold: float = 0.05):
    # Set the column names of the expression matrix to sample numbers starting from 1
    expression_data.columns = range(1, len(expression_data.columns) + 1)

    # Transpose the expression matrix and merge the cell type information into the gene expression matrix
    merged_data = expression_data.T
    merged_data['label'] = cell_types.set_index('index')['label']

    # Perform Wilcoxon rank-sum test and filter out significantly different genes
    significantly_different_genes = []
    for gene in expression_data.index:
        expression_data_temp = merged_data[gene]
        for cell_type in cell_types['label'].unique():
            current_type_expression = expression_data_temp[merged_data['label'] == cell_type]
            other_types_expression = expression_data_temp[merged_data['label'] != cell_type]

            # Perform Wilcoxon rank-sum test
            stat, p_value = ranksums(current_type_expression, other_types_expression)

            # If p-value is less than the specified threshold, record the significantly different gene
            if p_value < p_value_threshold:
                significantly_different_genes.append((gene, cell_type, p_value))

    # Convert the significantly different genes and their p-values to a DataFrame
    diff_genes_df = pd.DataFrame(significantly_different_genes, columns=['gene', 'label', 'p_value'])

    # Get the unique list of significantly different genes
    unique_genes = diff_genes_df['gene'].drop_duplicates().reset_index(drop=True)
    ranksums_gene_list = pd.DataFrame(unique_genes, columns=['gene'])

    # Generate a new gene expression matrix based on the filtered genes
    ranksums_matrix = expression_data.loc[ranksums_gene_list['gene'], :]

    # Return the list of significantly different genes and the expression matrix
    return ranksums_gene_list, ranksums_matrix


def Association_Score(source_cell_type: str, target_cell_type: str,
                      df_data: pd.DataFrame, CCC_list: pd.DataFrame,
                      abs_ccc: pd.DataFrame, threshold: float):
    # Filter source and target cell types
    filtered_CCC_list = CCC_list[(CCC_list['label_row'] == source_cell_type) &
                                 (CCC_list['label_column'] == target_cell_type)]

    # Calculate communication weights
    filtered_CCC_list['weight'] = filtered_CCC_list.apply(
        lambda row: abs_ccc.loc[row['Row'], row['Column']], axis=1)

    # Reset index
    filtered_CCC_list.index = range(len(filtered_CCC_list.index))

    # Get the corresponding sender and receiver cells
    send_cell_list = filtered_CCC_list['Row'].tolist()
    receive_cell_list = filtered_CCC_list['Column'].tolist()

    # iloc index starts from 0
    send_cell_list = [x - 1 for x in send_cell_list]
    receive_cell_list = [x - 1 for x in receive_cell_list]

    # Extract sender and receiver cell data from df_data
    send_cell_data = df_data.iloc[:, send_cell_list]
    send_cell_data.columns = range(0, len(send_cell_data.columns))
    print('send_cell_data:\n', send_cell_data)

    receive_cell_data = df_data.iloc[:, receive_cell_list]
    receive_cell_data.columns = range(0, len(receive_cell_data.columns))
    print('receive_cell_data:\n', receive_cell_data)

    # Count the number of non-zero elements in each row
    non_zero_counts_df1 = (send_cell_data != 0).sum(axis=1)
    non_zero_counts_df2 = (receive_cell_data != 0).sum(axis=1)

    # Filter rows where the number of zero elements is less than threshold * the number of cell pairs
    ccc_length = len(send_cell_list)
    filtered_indices_send = send_cell_data.index[non_zero_counts_df1 < (ccc_length * threshold)]
    filtered_indices_receive = receive_cell_data.index[non_zero_counts_df2 < (ccc_length * threshold)]

    # Drop these rows
    send_cell_data = send_cell_data.drop(index=filtered_indices_send)
    receive_cell_data = receive_cell_data.drop(index=filtered_indices_receive)

    # Reset index
    row = send_cell_data.index
    column = receive_cell_data.index
    send_cell_data.index = range(len(send_cell_data.index))
    receive_cell_data.index = range(len(receive_cell_data.index))
    print('final send_cell_data:\n', send_cell_data)
    print('final receive_cell_data:\n', receive_cell_data)

    # Create a zero matrix to store scores
    score_matrix = np.zeros((len(send_cell_data.index), len(receive_cell_data.index)))
    print('score_matrix: shape=', score_matrix.shape)

    # Calculate communication scores between cell pairs
    count = 1
    for i in range(score_matrix.shape[0]):
        print('Progress Bars: ',count,'/',score_matrix.shape[0])
        count += 1
        for j in range(score_matrix.shape[1]):
            score = 0
            for k in range(len(filtered_CCC_list.index)):
                score += filtered_CCC_list.loc[k, 'weight'] * np.log(
                    send_cell_data.loc[i, k] * receive_cell_data.loc[j, k] + 1)
            score /= len(filtered_CCC_list.index)
            score_matrix[i][j] = score

    # Generate the score matrix
    Absolute_Score = pd.DataFrame(score_matrix, index=row, columns=column)

    # Calculate weighted quantile means for each row and column
    row_means = 0.5 * Absolute_Score.quantile(0.5, axis=1) + \
                0.25 * (Absolute_Score.quantile(0.25, axis=1) + Absolute_Score.quantile(0.75, axis=1))

    column_means = 0.5 * Absolute_Score.quantile(0.5) + \
                   0.25 * (Absolute_Score.quantile(0.25) + Absolute_Score.quantile(0.75))

    # Calculate relative scores
    Relative_Score = Absolute_Score.copy()
    for i in range(Relative_Score.shape[0]):
        for j in range(Relative_Score.shape[1]):
            Relative_Score.iloc[i, j] = Relative_Score.iloc[i, j] - (row_means[i] + column_means[j])

    # Sort the relative scores and reset the index
    sorted_df = Relative_Score.stack(dropna=False).sort_values(ascending=False).reset_index()
    sorted_df.columns = ['Source_gene', 'Target_gene', 'RAS']

    return Absolute_Score, Relative_Score, sorted_df
