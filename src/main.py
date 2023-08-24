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
    st.title('Product Bundling :package:')
    st.markdown('Elevate Sales: Unleash Profitable Possibilities with Data-Driven Product Bundling!')
    
    # About section
    st.header('About :exclamation:')
    st.markdown("""
    Unlock the power of your transaction data to **uncover fascinating patterns** in customer behavior. This app is your key to **unveiling the perfect product pairs** that are often purchased together. With these insights at your fingertips, crafting irresistible product bundles becomes a breeze.
    Say goodbye to the uncertainty of ineffective bundling strategies – this app ensures you're always offering dynamic combinations that captivate your customers and drive sales! :smile:
    """)
    
    # How to use section
    st.header('How to use :question:')
    st.markdown("""
    1. Set your goal: Boost popular items or revitalize lesser-known products using the `Popular Items` table.
    2. Craft your pairing: Select 1 item from dropdown menu, then explore item synergies through the `Item Combinations` table.
    3. The higher the `Prob (%)`, the stronger the buying bond. Seize the opportunity and set the perfect price for your data-driven product bundles!
    Go try it yourself! :point_down:
    """)
    
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
        st.subheader('Popular Items :rice_ball:')
        sorted_popular_items_data = popular_items_data.sort_values(by='Trx A', ascending=False)
        st.dataframe(sorted_popular_items_data, hide_index=True)

    with col2:
        # Display item combinations table
        st.subheader(f'Item Combinations :fried_shrimp:')
        sorted_filtered_data = filtered_data.sort_values(by='Trx AB', ascending=False)
        
        # Adjust table width to fit content
        st.dataframe(sorted_filtered_data, hide_index=True)
        
    st.subheader("Here's your insight! :mag:")    
    st.markdown("""
    So, you select `{}`. Based on transaction data, your customer usually bought `{}` too with probability `{}%`. Easy isn't it?
    """.format(selected_item, sorted_filtered_data['Item B'].values[0], sorted_filtered_data['Prob (%)'].values[0]))
    
    # Expander for upgraded version
    with st.expander('Upgraded version :heavy_plus_sign:'):
        st.markdown("""
        You can upgrade the app to have third, fourth, and nth item! Additionally, you can have time selection, e.g., `Last 1 Month`, `Last 3 Month`, or `All Time`, so you can get relevant bundle idea that follows the current trend.
        """)
        
    # Contact information
    st.header('Interested in this app? :thought_balloon:')
    st.markdown("""
    Feel free to contact me via GitHub or email. I'll gladly help you to create this app for your business. Thanks for coming! :grin:
    """)

if __name__ == '__main__':
    main()
