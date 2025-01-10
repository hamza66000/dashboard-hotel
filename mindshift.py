import streamlit as st
import pandas as pd
import plotly.express as px

# Login Functionality
def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "hamza" and password == "dream123":  # Replace with secure authentication in production
            st.session_state["logged_in"] = True
        else:
            st.sidebar.error("Invalid username or password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    # Streamlit App Title
    st.title("Four Season Data Analysis Dashboard")
    st.sidebar.title("MindShift")
    st.sidebar.write("Explore different analyses:")
    st.image("Four-Seasons.jpg", width=200)

    # File Upload
    uploaded_file = st.file_uploader("Upload your file (csv, txt, xlsx, xls)", type=["csv", "txt", "xlsx", "xls"])
    if uploaded_file:
        # Load data based on file type
        if uploaded_file.name.endswith(".csv") or uploaded_file.name.endswith(".txt"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        # Convert Date columns to datetime
        data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
        data["CheckInDate"] = pd.to_datetime(data["CheckInDate"], errors='coerce')
        data["CheckOutDate"] = pd.to_datetime(data["CheckOutDate"], errors='coerce')

        # Navigation Options
        options = [
            "Overview",
            "Revenue Analysis",
            "Guest Analysis",
            "Seasonality",
            "Growth Trends",
            "Feedback Analysis",
        ]
        choice = st.sidebar.radio("Select a category", options)

        if choice == "Overview":
            st.header("Overview of the Dataset")
            st.dataframe(data.head())
            st.write("**Dataset Statistics**")
            st.write(data.describe())

        elif choice == "Revenue Analysis":
            st.header("Revenue Analysis")
            st.write(f"**Total Revenue:** ${data['TotalRevenue'].sum():,.2f}")

            # Revenue by Quarter
            data['Quarter'] = data['Date'].dt.to_period("Q").astype(str)
            revenue_by_quarter = data.groupby("Quarter")["TotalRevenue"].sum().reset_index()
            st.write("**Quarterly Revenue:**")
            fig = px.bar(revenue_by_quarter, x="Quarter", y="TotalRevenue", title="Total Revenue per Quarter", text="TotalRevenue")
            st.plotly_chart(fig)
            st.write("This chart shows how much revenue the hotel earned in each quarter of the year.")

            # Annual Revenue
            data['Year'] = data['Date'].dt.year
            revenue_by_year = data.groupby("Year")["TotalRevenue"].sum().reset_index()
            fig = px.line(revenue_by_year, x="Year", y="TotalRevenue", title="Total Revenue per Year")
            st.plotly_chart(fig)
            st.write("This chart shows the total yearly revenue, helping to identify trends over time.")

        elif choice == "Guest Analysis":
            st.header("Guest Analysis")
            # Nationality Distribution
            nationality_distribution = data["Nationality"].value_counts().reset_index()
            nationality_distribution.columns = ["Nationality", "Count"]
            fig = px.pie(nationality_distribution, values="Count", names="Nationality", title="Nationality Distribution")
            st.plotly_chart(fig)
            st.write("This pie chart shows the proportion of guests from different nationalities staying at the hotel.")

            # Age Group Analysis
            age_group_distribution = data["AgeGroup"].value_counts().reset_index()
            age_group_distribution.columns = ["AgeGroup", "Count"]
            fig = px.bar(age_group_distribution, x="AgeGroup", y="Count", title="Age Group Distribution", text="Count")
            st.plotly_chart(fig)
            st.write("This chart shows how many guests belong to different age groups, helping to understand the demographics.")

        elif choice == "Seasonality":
            st.header("Seasonality Analysis")
            data['Month'] = data['Date'].dt.month
            revenue_by_month = data.groupby("Month")["TotalRevenue"].sum().reset_index()
            fig = px.line(revenue_by_month, x="Month", y="TotalRevenue", title="Seasonality of Revenue", markers=True)
            st.plotly_chart(fig)
            st.write("This chart highlights how revenue fluctuates across different months, revealing seasonal trends.")

        elif choice == "Growth Trends":
            st.header("Growth Trends")

            # Monthly Growth Analysis
            revenue_monthly = data.groupby(data["Date"].dt.to_period("M").astype(str))["TotalRevenue"].sum().reset_index()
            revenue_monthly.columns = ["Month", "TotalRevenue"]
            fig = px.bar(revenue_monthly, x="Month", y="TotalRevenue", title="Monthly Growth in Revenue")
            st.plotly_chart(fig)
            st.write("This chart shows the revenue growth on a monthly basis, helping to analyze short-term trends.")

            # Yearly Growth Analysis
            revenue_yearly = data.groupby(data["Date"].dt.year)["TotalRevenue"].sum().reset_index()
            revenue_yearly.columns = ["Year", "TotalRevenue"]
            fig = px.bar(revenue_yearly, x="Year", y="TotalRevenue", title="Yearly Growth in Revenue")
            st.plotly_chart(fig)
            st.write("This chart shows the revenue growth on a yearly basis, revealing long-term performance trends.")

        elif choice == "Feedback Analysis":
            st.header("Guest Feedback Analysis")
            # GuestFeedbackScore Distribution
            fig = px.histogram(data, x="GuestFeedbackScore", title="Feedback Score Distribution", nbins=10)
            st.plotly_chart(fig)
            st.write("This chart shows how guests rated their stay, helping to identify overall satisfaction.")

            # Comparison of Spa, Gym Access, and Events
            if "SpaChannel" in data.columns:
                fig = px.box(data, x="SpaChannel", y="GuestFeedbackScore", title="Spa Usage and Feedback Comparison")
                st.plotly_chart(fig)
                st.write("This chart compares feedback scores based on whether guests used the spa or other services.")

            # LoyaltyTier vs Feedback
            if "LoyaltyTier" in data.columns:
                loyalty_feedback = data.groupby("LoyaltyTier")["GuestFeedbackScore"].mean().reset_index()
                fig = px.bar(loyalty_feedback, x="LoyaltyTier", y="GuestFeedbackScore", title="Loyalty Tier vs Feedback Score")
                st.plotly_chart(fig)
                st.write("This chart shows how feedback scores differ among guests based on their loyalty tier.")

        st.sidebar.write("For inquiries, contact us at MindShift.")
    else:
        st.write("Please upload a valid file to get started.")
