import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
from sqlalchemy import create_engine, text

begin = st.container()

st.title("Food waste management system")  
st.sidebar.title("Select your option")

# Capture user's sidebar selection
selected_option = st.sidebar.radio(
    "Select your option",
    options=[
        "Project Introduction",
        "View Tables",
        "CRUD Operations",
        "SQL Queries & Visualization",
        "Learner SQL queries",
        "User Introduction"
    ],
    index=0,
    key="sidebar_radio"
)

# Display content based on selection
if selected_option == "Project Introduction":
    st.write("This project helps manage surplus food and reduce wastage by connecting providers and receivers")

elif selected_option == "View Tables":

    option = st.selectbox(
        "Select the dataset to view the records:",
        ["providers_data", "receivers_data", "claims_data","Food_listings_data"]
    )
    if option == "providers_data":
        df = pd.read_csv(r'C:\Users\balam\Guvi\Miniproject\providers_data.csv')
        filtered_df = dataframe_explorer(df)
        st.dataframe(filtered_df, use_container_width=True)
        
    elif option == "receivers_data":
        df = pd.read_csv(r'C:\Users\balam\Guvi\Miniproject\receivers_data.csv')
        filtered_df = dataframe_explorer(df)
        st.dataframe(filtered_df, use_container_width=True)

    elif option == "claims_data":
        df = pd.read_csv(r'C:\Users\balam\Guvi\Miniproject\claims_data.csv')
        filtered_df = dataframe_explorer(df)
        st.dataframe(filtered_df, use_container_width=True)

    elif option == "Food_listings_data":
        df = pd.read_csv(r'C:\Users\balam\Guvi\Miniproject\claims_data.csv')
        filtered_df = dataframe_explorer(df)
        st.dataframe(filtered_df, use_container_width=True)


elif selected_option == "CRUD Operations":
    st.write("CRUD operations will be implemented here.")
    crud_option = st.selectbox(
        "Select the operation:",
        ["Add", "Update", "Delete"]
    
    )
    # 🔌 Connect to PostgreSQL
    DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
    engine = create_engine(DATABASE_URL, echo=True)

    if crud_option == "Add":
        try:
            
            
            with st.form(key="add_food_form"):
                st.write("Fill in the details to add a new food item:")
                food_name = st.selectbox(
                    "Select the items to add:",
                    ["Chicken", "Dairy", "Fish", "Fruits", "Pasta", "Rice", "Salad", "Soup", "Vegetables", "Bread"]
                )
                food_id = st.number_input('food_id', min_value=1, step=2)
                quantity = st.number_input('Quantity', min_value=1, step=2)
                
                provider_id = st.number_input('Provider ID', min_value=1, step=1)
                st.write(f"Quantity type: {type(quantity)}")     # should be <class 'int'>
                st.write(f"Provider ID type: {type(provider_id)}")
                st.write(f"food_namee: {type(food_name)}")
                if isinstance(quantity, str):
                    quantity = int(quantity)
                if isinstance(provider_id, str):
                    provider_id = int(provider_id)

                    # should be <class 'int'>
                submitted = st.form_submit_button("Submit")
                
            if submitted:
                query1 = '''INSERT INTO food_listings_data(food_id,food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type) 
                        VALUES (:food_id, :food_name, :quantity, :expiry_date, :provider_id, :provider_type, :location, :food_type,:meal_type);'''
                values = {
                "food_id": food_id,    
                "food_name": food_name,
                "quantity": quantity,
                "expiry_date": "2025-07-31",  # Example expiry date, you can change it as needed
                "provider_id": provider_id,
                "provider_type": "Grocery Store",
                "location": "South Kellyville",
                "food_type": "Nonveg",
                "meal_type": "dinnder"
                }

                with engine.connect() as conn:
                    conn.execute(text(query1), values)
                    print(values)
                
                print("✅ Data Added in PostgreSQL!")
                st.success("Data Added in PostgreSQL!")

        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            st.error(f"Error creating tables: {e}")

    elif crud_option == "Update":
        st.write("Update operation will be implemented here.")
        
        with st.form(key="Update_food_form"):
            st.write("Fill in the details to Update existing food item:")
            food_id = st.number_input('food_id', min_value=1, step=1)
            quantity = st.number_input('quantity', min_value=1, step=1)
            data = {
                "food_id": food_id,
                "quantity": quantity
            }
            update = st.form_submit_button("Update")
                
        if update:
            with engine.connect() as conn:
                conn.execute(text('UPDATE food_listings_data SET "quantity" = :quantity WHERE "food_id" = :food_id'), data)
                conn.commit()
                st.success("Data Updated in PostgreSQL!")
        
    elif crud_option == "Delete":
        st.write("Delete operation will be implemented here.")
        
        with st.form(key="Delete_Form"):
            st.write("Enter the food id to delete details")
            food_id = st.number_input('food_id', min_value=1, step=1)
            
            delete = st.form_submit_button("delete")
                
        if delete:
            
            with engine.connect() as conn:
                conn.execute(text('DELETE FROM food_listings_data WHERE "food_id" = :food_id'),
                {'food_id': food_id})
                conn.commit()
            print("Data Deleted Successfully!")
            st.success("Data Deleted Successfully!")
    
elif selected_option == "SQL Queries & Visualization":
    st.write("SQL queries and visualization will be implemented here.")
      # 🔌 Connect to PostgreSQL
   

    option = st.selectbox(
        "Select the query to view the records:",
        ["Q1 providers_data&Receivers_count", 
         "Q2 total food quantity", 
         "Q3 contact information of food providers in a specific city",
         "Q4 Which receivers have claimed the most food",
         "Q5 receivers have claimed the most food",
         "Q6 total quantity of food available from all providers",
         "Q7 city has the highest number of food listings",
         "Q8 most commonly available food types",
         "Q9 highest number of successful food claims",
         "Q10 percentage of food claims are completed vs. pending vs. canceled",
         "Q11 What is the average quantity of food claimed per receiver",
         "Q12 Which meal type (breakfast, lunch, dinner, snacks) is claimed the most",
         "Q13 What is the total quantity of food donated by each provider"]
    )
    if option == "Q1 providers_data&Receivers_count":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT count(provider_id) as Providers,p.city as P_city,Count(receiver_id) as Receivers,r.city as R_city
                FROM providers_data as p
                FULL OUTER join receivers_data as r
                on p.city=r.city
                group by p.city,r.city,r.receiver_id
                Order by p.city;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
    elif option == "Q2 total food quantity":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT SUM(quantity)as total,provider_type from food_listings_data
                GROUP BY provider_type
                ORDER BY total DESC
                LIMIT 1;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
    elif option == "Q3 contact information of food providers in a specific city":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT Name, Type, Address, Contact
                FROM providers_data
                WHERE City = 'New Jessica';
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
    elif option == "Q4 Which receivers have claimed the most food":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT r.type,r.name, count(claim_id) as Total_Claims
                FROM claims_data c
                INNER JOIN receivers_data r
                ON c.receiver_id=r.receiver_id
                WHERE status='Completed'
                GROUP BY r.type,r.name
                ORDER BY Total_Claims DESC
                LIMIT 5;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
    elif option == "Q5 receivers have claimed the most food":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT SUM(quantity) AS Total_Quantity
                FROM food_listings_data;"""
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
    elif option == "Q6 total quantity of food available from all providers":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT Location, COUNT(*) AS Listings_Count
                FROM food_listings_data
                GROUP BY Location
                ORDER BY Listings_Count DESC
                LIMIT 1;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
            
    elif option == "Q7 city has the highest number of food listings":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT Food_Type, COUNT(*) AS Count
                FROM food_listings_data
                GROUP BY Food_Type
                ORDER BY Count DESC;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
            
    elif option == "Q8 most commonly available food types":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        
        query= """SELECT fl.Food_Name, COUNT(c.Claim_ID) AS Claim_Count
                FROM claims_data c
                JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
                GROUP BY fl.Food_Name
                ORDER BY Claim_Count DESC;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
    elif option == "Q9 highest number of successful food claims":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
                FROM claims_data c
                JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
                JOIN providers_data p ON fl.Provider_ID = p.Provider_ID
                WHERE c.Status = 'Completed'
                GROUP BY p.Name
                ORDER BY Successful_Claims DESC
                LIMIT 1;
    """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
    elif option == "Q10 percentage of food claims are completed vs. pending vs. canceled":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        
        query= """SELECT Status, 
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data), 2) AS Percentage
                FROM claims_data
                GROUP BY Status;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
            
    elif option == "Q11 What is the average quantity of food claimed per receiver":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT r.Name, AVG(fl.Quantity) AS Avg_Quantity_Claimed
                    FROM claims_data c
                    JOIN receivers_data r ON c.Receiver_ID = r.Receiver_ID
                    JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
                    WHERE c.Status = 'Completed'
                    GROUP BY r.Name
                    ORDER BY Avg_Quantity_Claimed DESC
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
                 
    elif option == "Q12 Which meal type (breakfast, lunch, dinner, snacks) is claimed the most":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS Claim_Count
                FROM claims_data c
                JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
                WHERE c.Status = 'Completed'
                GROUP BY fl.Meal_Type
                ORDER BY Claim_Count DESC;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
    elif option == "Q13 What is the total quantity of food donated by each provider":
       
        DATABASE_URL = "postgresql://postgres:root@localhost:5432/food_waste_manage"
        engine = create_engine(DATABASE_URL, echo=True)
        query= """SELECT p.Name, SUM(fl.Quantity) AS Total_Donated
                    FROM food_listings_data fl
                    JOIN providers_data p ON fl.Provider_ID = p.Provider_ID
                    GROUP BY p.Name
                    ORDER BY Total_Donated DESC;
                """
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
           # filtered_df = dataframe_explorer(df)
            st.dataframe(df, use_container_width=True)
            
            
# Display content based on selection
elif selected_option == "User Introduction":
    st.write("I am Balamurugan, Aspiring Data scientist and this is my first data science project")