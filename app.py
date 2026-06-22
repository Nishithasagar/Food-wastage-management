import streamlit as st
import pandas as pd
import plotly.express as px

food_df = pd.read_csv("food_listings_data.csv")
providers_df = pd.read_csv("providers_data.csv")
receivers_df = pd.read_csv("receivers_data.csv")
claims_df = pd.read_csv("claims_data.csv")

st.set_page_config(
    page_title="Food Wastage Management",
    page_icon="♻️",
    layout="wide"
)

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0F172A;
    color: white;
}
/* Main Content Area */
.main .block-container {
    background-color: #111827;
    border-radius: 15px;
    padding: 2rem;
}
/* Sidebar */
section[data-testid="stSidebar"] > div {
    padding-top: 50px;
    background-color: #1E3A5F;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Header Sizes & Colors */
h1 {
    font-size: 42px !important;
    color: #FFFFFF !important;
}

h2 {
    font-size: 32px !important;
    color: #60A5FA !important;
}

h3 {
    font-size: 24px !important;
    color: #93C5FD !important;
}

/* KPI Cards */
div[data-testid="metric-container"] {
    background-color: #F8FAFC;
    border: 2px solid #3B82F6;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
}

/* Metric Values */
div[data-testid="metric-container"] label,
div[data-testid="metric-container"] div {
    color: #0B7A3E !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <h2 style='font-size:36px;'>
    ♻️ Food Wastage Management
    </h2>
    """, unsafe_allow_html=True
)

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Project Overview",
        "📊 Dashboard",
        "🗄️ SQL Analysis",
        "📈 EDA Analysis",
        "🔍 Filter & Search",
        "✏️ CRUD Operations",
        "📋 Data Tables",
        "💡 Insights & Recommendations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Python . MySQL . Streamlit")

# ---------------- DASHBOARD PAGE ---------------- #

if page == "📊 Dashboard":
    st.markdown("""
        <h1 style='font-size:38px;'>
        ♻️ Food Wastage Management Dashboard
        </h1>
        """, unsafe_allow_html=True)
    
    st.caption("Connecting Surplus Food with Communities in Need")

    st.markdown("""
        ### Reducing Food Waste Through Efficient Redistribution

        This dashboard provides insights into food donations, providers,
        receivers, claims, and food distribution trends.
        """)
    
    # KPI Queries
    food_count = len(food_df)

    provider_count = len(providers_df)

    receiver_count = len(receivers_df)

    claims_count = len(claims_df)

    # KPI Cards
    st.markdown("""
        <h2 style='font-size:32px;'>
        📊 Key Performance Indicators
        </h2>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🍱 Food Listings",
            value=food_count
        )

    with col2:
        st.metric(
            label="🏢 Providers",
            value=provider_count
        )

    with col3:
        st.metric(
            label="🤝 Receivers",
            value=receiver_count
        )

    with col4:
        st.metric(
            label="📄 Claims",
            value=claims_count
        )

# ---------------- DISTRIBUTION ANALYSIS ----------------

    st.markdown("---")
    st.subheader("📊 Distribution Analysis")

    col5, col6 = st.columns([1, 1], gap="large")

    food_type = food_df["Food_Type"].value_counts().reset_index()
    food_type.columns=["Food_Type","count"]

    provider_type = providers_df["Type"].value_counts().reset_index()
    provider_type.columns=["Type","count"]

    with col5:
        fig = px.pie(
            food_type,
            names='Food_Type',
            values='count',
            hole=0.5,
            title="Food Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        fig = px.pie(
            provider_type,
            names='Type',
            values='count',
            hole=0.5,
            title="Provider Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- CLAIMS ANALYSIS ----------------

    st.markdown("---")
    st.subheader("📈 Claims Analysis")

    col7, col8 = st.columns([1, 1], gap="large")

    status_data = claims_df["Status"].value_counts().reset_index()
    status_data.columns=["Status","count"]

    food_df["Expiry_Date"] = pd.to_datetime(
        food_df["Expiry_Date"],
        errors="coerce"
    )

    expired_data = food_df.copy()

    expired_data["status"] = expired_data["Expiry_Date"].apply(
        lambda x: "EXPIRED"
        if pd.notnull(x) and x < pd.Timestamp.today()
        else "AVAILABLE"
    )

    expired_data = (
    expired_data["status"]
        .value_counts()
        .rename_axis("status")
        .reset_index(name="count")
    )

    with col7:
        fig = px.pie(
            status_data,
            names='Status',
            values='count',
            hole=0.5,
            title="Claim Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col8:
        expired_counts = food_df["Expiry_Date"].notna().value_counts()

        fig = px.pie(
            names=["AVAILABLE", "EXPIRED"],
            values=[
                expired_counts.get(True, 0),
                expired_counts.get(False, 0)
            ],
            hole=0.5,
            title="Expired vs Available Food"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- GEOGRAPHIC ANALYSIS ----------------

    st.markdown("---")
    st.subheader("📍 Geographic Analysis")

    col9, col10 = st.columns(2)

    city_data = providers_df["City"].value_counts().reset_index()
    city_data.columns=["City","count"]
    city_data = city_data.head(10)

    claim_city_data = (
        providers_df["City"]
        .value_counts()
        .reset_index()
    )

    claim_city_data.columns = ["City", "total_claims"]

    claim_city_data = claim_city_data.head(10)

    with col9:
        st.bar_chart(city_data.set_index("City"))

    with col10:
        st.bar_chart(claim_city_data.set_index("City"))

# ---------------- SQL ANALYSIS PAGE ---------------- #

elif page == "🗄️ SQL Analysis":

    st.title("📊 SQL Analysis")
    
    query_option = st.selectbox(
        "Select Analysis",
        [
            "Top Providers by Claims",
            "Top Receivers by Claims",
            "Providers by City",
            "Food Type Distribution",
            "Expired Food Count",
            "Expired vs Available Food",
            "Most Claimed Foods",
            "Claim Status Distribution",
            "Provider Type Distribution",
            "Meal Type Distribution",
            "Top Locations by Food Listings",
            "Claims by Provider City",
            "Total Food Quantity by Provider Type",
            "Average Quantity by Food Type",
            "Top Cities by Food Listings"
        ]
    )
    if query_option == "Top Providers by Claims":
        
        result = (
            providers_df["Name"]
            .value_counts()
            .reset_index()
        )

        result.columns=["name","total_claims"]
        result=result.head(10)

        st.dataframe(result)

        st.bar_chart(
        result.set_index("name")
        )

        st.success(
        "These providers are associated with the highest number of food claims."
        )
    elif query_option == "Top Receivers by Claims":

        result = (
            receivers_df["Name"]
            .value_counts()
            .reset_index()
        )

        result.columns=["name","total_claims"]
        result=result.head(10)

        st.dataframe(result)
        st.bar_chart(result.set_index("name"))

        st.success("Top receivers based on number of food claims.")
    elif query_option == "Providers by City":

         result = (
            providers_df["City"]
            .value_counts()
            .reset_index()
        )

         result.columns=["city","total_providers"]

         st.dataframe(result)
         st.bar_chart(result.set_index("city"))

         st.success("Shows cities with the highest number of food providers.")
    elif query_option == "Food Type Distribution":

        result = (
            food_df["Food_Type"]
            .value_counts()
            .reset_index()
        )

        result.columns=["food_type","total"]

        st.dataframe(result)
        fig=px.pie(
            result,
            names="food_type",
            values="total",
            hole=0.5,
            title="Food Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("Distribution of food listings by food type.")
    elif query_option == "Expired Food Count":

        food_df["Expiry_Date"]=pd.to_datetime(
        food_df["Expiry_Date"],
        errors="coerce"
        )

        result=pd.DataFrame({
            "expired_food":[
            (food_df["Expiry_Date"]<
             pd.Timestamp.today()).sum()
            ]
        })

        st.dataframe(result)

        st.success("Total number of expired food listings.")
    elif query_option == "Expired vs Available Food":

        result=food_df.copy()

        result["status"]=result["Expiry_Date"].apply(
            lambda x:
            "EXPIRED"
            if pd.notnull(x)
            and pd.to_datetime(x,errors="coerce")
            < pd.Timestamp.today()
            else "AVAILABLE"
        )

        result=(
            result["status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="total")
        )

        st.dataframe(result)
        fig=px.pie(
            result,
            names="status",
            values="total",
            hole=0.5,
            title="Expired vs Available Food"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success(
            "All food items in the dataset have expiry dates in March 2025; therefore, they are currently classified as expired."
        )
    elif query_option == "Most Claimed Foods":
        
        result = (
            food_df["Food_Name"]
            .value_counts()
            .reset_index()
        )

        result.columns = ["food_name", "total_claims"]

        result = result.head(10)

        st.dataframe(result)

        st.bar_chart(
        result.set_index("food_name")
        )

        st.success(
        "Most frequently claimed food items."
        )
    elif query_option == "Claim Status Distribution":

        result=(
            claims_df["Status"]
            .value_counts()
            .reset_index()
        )

        result.columns=["status","total"]

        st.dataframe(result)
        fig=px.pie(
            result,
            names="status",
            values="total",
            hole=0.5,
            title="Claim Status Distribution"
        )
        st.plotly_chart(fig,use_container_width=True)
        st.success("Distribution of claim statuses.")
    elif query_option == "Provider Type Distribution":

        result=(
            providers_df["Type"]
            .value_counts()
            .reset_index()
        )

        result.columns=["type","total"]

        st.dataframe(result)
        fig=px.pie(
            result,
            names="type",
            values="total",
            hole=0.5,
            title="Provider Type Distribution"
        )
        st.plotly_chart(fig,use_container_width=True)
        st.success("Distribution of provider types.")
    elif query_option == "Meal Type Distribution":

        result=(
            food_df["Meal_Type"]
            .value_counts()
            .reset_index()
        )

        result.columns=["meal_type","total"]

        st.dataframe(result)

        fig = px.pie(
            result,
            names="meal_type",
            values="total",
            hole=0.5,
            title="Meal Type Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success("Distribution of food listings by meal type.")
    elif query_option == "Top Locations by Food Listings":

        result=(
            food_df["Location"]
            .value_counts()
            .reset_index()
        )

        result.columns=["location","total_food"]

        result=result.head(10)

        st.dataframe(result)

        st.bar_chart(
            result.set_index("location")
        )

        st.success("Top locations based on food listings.")    
    elif query_option == "Claims by Provider City":

        result=(
            providers_df["City"]
            .value_counts()
            .reset_index()
        )

        result.columns=["city","total_claims"]

        st.dataframe(result)
        st.bar_chart(result.set_index("city"))

        st.success("Cities generating the highest number of food claims.")
    elif query_option == "Total Food Quantity by Provider Type":

        result = (
            providers_df.groupby("Type")
            .size()
            .reset_index(name="total_quantity")
        )

        st.dataframe(result)

        st.bar_chart(
        result.set_index("Type")
        )

        st.success(
        "Total food quantity grouped by provider type."
        )
    elif query_option == "Average Quantity by Food Type":

        result = (
            food_df.groupby("Food_Type")["Quantity"]
            .mean()
            .reset_index()
        )

        result.columns = [
            "Food_Type",
            "Average_Quantity"
        ]

        st.dataframe(result)

        st.bar_chart(
        result.set_index("Food_Type")
        )

        st.success(
        "Average quantity available for each food type."
        )
    elif query_option == "Top Cities by Food Listings":

        result = (
            food_df["Location"]
            .value_counts()
            .reset_index()
        )

        result.columns = [
            "City",
            "Total_Listings"
        ]

        result = result.head(10)

        st.dataframe(result)

        st.bar_chart(
        result.set_index("City")
        )

        st.success(
        "Top cities with the highest food listings."
        )

# ---------------- EDA PAGE ---------------- #

elif page == "📈 EDA Analysis":

    st.title("📈 Exploratory Data Analysis")

# ---------------- FOOD TYPE ----------------

    food_type = (
        food_df["Food_Type"]
        .value_counts()
        .reset_index()
    )

    food_type.columns = [
        "food_type",
        "count"
    ]

    st.subheader("🍱 Food Type Distribution")

    st.bar_chart(
        food_type.set_index("food_type")
    )

# ---------------- MEAL TYPE ----------------

    meal_type = (
        food_df["Meal_Type"]
        .value_counts()
        .reset_index()
    )

    meal_type.columns = [
        "meal_type",
        "count"
    ]

    st.subheader("🍽 Meal Type Distribution")

    st.bar_chart(
        meal_type.set_index("meal_type")
    )

# ---------------- QUANTITY ----------------

    quantity_data = (
        food_df[["Quantity"]]
    )

    st.subheader(
        "📦 Food Quantity Distribution"
    )

    st.bar_chart(
        quantity_data
    )

# ---------------- PROVIDER TYPE ----------------

    provider_type = (
        providers_df["Type"]
        .value_counts()
        .reset_index()
    )

    provider_type.columns = [
        "type",
        "count"
    ]

    st.subheader(
        "🏢 Provider Type Distribution"
    )

    st.bar_chart(
        provider_type.set_index("type")
    )

# ---------------- CITY ----------------

    city_data = (
        providers_df["City"]
        .value_counts()
        .reset_index()
    )

    city_data.columns = [
        "city",
        "count"
    ]

    city_data = city_data.head(10)

    st.subheader(
        "📍 Top Provider Cities"
    )

    st.bar_chart(
        city_data.set_index("city")
    )

# ---------------- INSIGHTS ----------------

    st.subheader(
        "🔍 Key Insights"
    )

    st.info("""
    • Food donations are concentrated in a few provider categories.

    • Certain food types dominate the listings.

    • Some cities contribute significantly more donations.

    • Claim activity shows active redistribution of food.

    • Quantity distribution varies across providers.
    """)

# ---------------- FILTER & SEARCH PAGE ---------------- #

elif page == "🔍 Filter & Search":

    st.title("🔍 Filter & Search")

# ---------------- SEARCH FOOD ----------------

    st.subheader("Search Food")

    food_name = st.text_input(
        "Enter Food Name"
    )

    if food_name:

        search_result = food_df[
            food_df["Food_Name"]
            .str.contains(
                food_name,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            search_result
        )

# ---------------- FILTER CITY ----------------

    st.subheader(
        "Filter by City"
    )

    cities = sorted(
        providers_df["City"]
        .dropna()
        .unique()
    )

    selected_city = st.selectbox(
        "Select a City",
        cities
    )

    city_result = providers_df[
        providers_df["City"]
        == selected_city
    ]

    st.dataframe(
        city_result
    )

    csv = city_result.to_csv(
        index=False
    )

    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="providers_data.csv",
        mime="text/csv"
    )

# ---------------- FILTER FOOD TYPE ----------------

    st.subheader(
        "Filter by Food Type"
    )

    food_types = sorted(
        food_df["Food_Type"]
        .dropna()
        .unique()
    )

    selected_food_type = st.selectbox(
        "Select Food Type",
        food_types
    )

    food_type_result = food_df[
        food_df["Food_Type"]
        == selected_food_type
    ]

    st.dataframe(
        food_type_result
    )

# ---------------- FILTER PROVIDER ----------------

    st.subheader(
        "Filter by Provider"
    )

    providers = sorted(
        providers_df["Name"]
        .dropna()
        .unique()
    )

    selected_provider = st.selectbox(
        "Select Provider",
        providers
    )

    provider_result = providers_df[
        providers_df["Name"]
        == selected_provider
    ]

    st.dataframe(
        provider_result
    )
#------------------- CRUD Operations -------------------- #

elif page == "✏️ CRUD Operations":

    st.title("✏️ CRUD Operations")

# Initialize session storage

    if "food_data" not in st.session_state:
        st.session_state.food_data = food_df.copy()

# ---------------- CREATE ----------------

    st.subheader("➕ Add New Food Listing")

    food_name = st.text_input(
        "Food Name"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1
    )

    if st.button("Add Food"):

        new_row = pd.DataFrame({
            "Food_Name": [food_name],
            "Quantity": [quantity]
        })

        st.session_state.food_data = pd.concat(
            [
                st.session_state.food_data,
                new_row
            ],
            ignore_index=True
        )

        st.success(
            "Food Added Successfully"
        )

# ---------------- UPDATE ----------------

    st.markdown("---")

    st.subheader(
        "✏️ Update Food Quantity"
    )

    update_name = st.text_input(
        "Enter Food Name"
    )

    new_quantity = st.number_input(
        "New Quantity",
        min_value=1,
        key="update_qty"
    )

    if st.button("Update"):

        st.session_state.food_data.loc[
            st.session_state.food_data["Food_Name"]
            == update_name,
            "Quantity"
        ] = new_quantity

        st.success(
            "Record Updated"
        )

# ---------------- DELETE ----------------

    st.markdown("---")

    st.subheader(
        "🗑 Delete Food Listing"
    )

    delete_name = st.text_input(
        "Food Name To Delete"
    )

    if st.button("Delete"):

        st.session_state.food_data = (
            st.session_state.food_data[
                st.session_state.food_data[
                    "Food_Name"
                ]
                != delete_name
            ]
        )

        st.success(
            "Record Deleted"
        )

# ---------------- PREVIEW ----------------

    st.markdown("---")

    st.subheader(
        "📋 Current Data"
    )

    st.dataframe(
        st.session_state.food_data
    )

#-------------------------- DATA TABLES ---------------------- #

elif page == "📋 Data Tables":

    st.title("📋 Data Tables")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🍱 Food Listings",
            "🏢 Providers",
            "🙋 Receivers",
            "📄 Claims"
        ]
    )

# ---------------- FOOD ----------------

    with tab1:
        st.dataframe(
            food_df
        )

# ---------------- PROVIDERS ----------------

    with tab2:
        st.dataframe(
            providers_df
        )

# ---------------- RECEIVERS ----------------

    with tab3:
        st.dataframe(
            receivers_df
        )

# ---------------- CLAIMS ----------------

    with tab4:
        st.dataframe(
            claims_df
        )



