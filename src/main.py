import pandas as pd
import streamlit as st

def popular_items(data):
    """
    Calculate the number of unique transactions (Trx A) for each item (Item A).

    Args:
        data (pandas.DataFrame): Input DataFrame containing transaction data.

    Returns:
        pandas.DataFrame: DataFrame with item names and their corresponding unique transaction counts.
    """
    # Rename column 'Item' to 'Item A'
    data = data.rename(columns={'Item': 'Item A'})

    # Calculate the number of unique transactions for each item
    data = data.groupby(['Item A']).agg({'TransactionID': 'nunique'})
    data = data.reset_index()
    data = data.rename(columns={'TransactionID': 'Trx A'})

    return data

def create_combinations(data):
    """
    Create combinations of items (Item A and Item B) and calculate transaction-related statistics.

    Args:
        data (pandas.DataFrame): Input DataFrame containing transaction data.

    Returns:
        pandas.DataFrame: DataFrame with combinations of items and calculated statistics.
    """
    # Rename column 'Item' to 'Item A'
    data1 = data.rename(columns={'Item': 'Item A'})

    # Rename column 'Item' to 'Item B'
    data2 = data.rename(columns={'Item': 'Item B'})

    # Merge data1 and data2 based on 'TransactionID' and filter out self-combinations
    data12 = pd.merge(data1, data2, how='left', on=['TransactionID'])
    data12 = data12[data12['Item A'] != data12['Item B']]

    # Calculate the number of unique transactions (Trx AB) for each item combination
    data2 = data12.groupby(['Item A', 'Item B']).agg({'TransactionID': 'nunique'})
    data2 = data2.reset_index()
    data2 = data2.rename(columns={'TransactionID': 'Trx AB'})

    # Merge data2 and data1 to calculate probability and other metrics
    comb = pd.merge(data2, popular_items(data1), how='left', on=['Item A'])
    comb['Prob (%)'] = round(comb['Trx AB'] / comb['Trx A'], 3) * 100

    return comb

# Streamlit app
def main():
    st.title('Product Bundling App')

    # Read data from CSV file
    data = pd.read_csv('./data/groceries_dataset.csv')

    # Calculate popular items
    popular_items_data = popular_items(data)

    # Item selection
    top_item_index = int(popular_items_data.sort_values(by='Trx A', ascending=False).index[0])
    selected_item = st.selectbox('Select an item:', popular_items_data['Item A'], index=top_item_index)

    # Calculate item combinations and statistics for the selected item
    item_combinations = create_combinations(data)

    # Filter data based on the selected item
    filtered_data = item_combinations[item_combinations['Item A'] == selected_item]

    # Use columns layout to display tables side by side
    col1, col2 = st.columns([0.4, 0.6], gap='large')

    with col1:
        # Display popular items table
        st.subheader('Popular Items')
        sorted_popular_items_data = popular_items_data.sort_values(by='Trx A', ascending=False)
        st.dataframe(sorted_popular_items_data, hide_index=True)

    with col2:
        # Display item combinations table
        st.subheader(f'Item Combinations')
        sorted_filtered_data = filtered_data.sort_values(by='Trx AB', ascending=False)
        
        # Adjust table width to fit content
        st.dataframe(sorted_filtered_data, hide_index=True)

if __name__ == '__main__':
    main()
