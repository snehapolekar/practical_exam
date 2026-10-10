import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Expensetracker:
    def __init__(self,filename=expense.csv):
        self.filename = filenameself
        self.valid_catagories = ['Food' , 'Transport' , 'Utilities' , 'Entertainment' , 'Shopping' , 'Other']
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            self.df = pd.read_csv(self.filename)
            self.df['Date'] = pd.to_datetime(self.df['date'])
            self.df['Amount'] = pd.to_numeric(self.df['Amount'],errors = 'coerce')
            self.df.dropna(subset = ['Date' , 'Amount' , 'Category'] , inplace = True)

        else:
            self.df = pd.DataFrame(coloumns = ['Date' , 'Amount' , 'Category' , 'Description'])

    def add_expense(self,date,amount,category,description):
        try:
            amount = float(amount)
            if amount <= 0:
                print("Error :Invalid Amount! please enter positve amount!! ")
                return False

            category = category.capitalize()
            if category not in self.valid_categories:
                print(f"Error : Invalid Category. Valid categories:{self.valid_categories}")
                return False

            date_val = pd.to_datetime(date)
            new_row = pd.DataFrame([{
                'Date' = date_val,
                'Amount' = amount,
                'Category' =  category,
                'Description' = description
            }])
                
            

            self.df = pd.concat(self.filename,index = False)
            print("Expense successfully added!!")
            return True

        except ValueError :
            print("Error:Invalid DAte or Amount format!!")
            return False

    def get_summary(self):
        if self.df.empty:
            print("No expense data available.")
            return

        amounts = self.df['Amount'].values
        total_expense = np.sum(amounts)
        avg_expense = np.mean(amounts)

        print("\n ------- Expense Summary -------")
        print("Totai Expense , {total_expense:.2f}")
        print("Average expense : {avg_expense:.2f}")

        # Group by Category using pandas

        category_summary = self.df.groupby('category')['Amount'].sum()
        print("\n Expense by Category:")

    print(category_summary.to_string())

    def filter_expenses(self,category = None , min_amount = None) :

        filtered_df = self.df.copy()

        if category:
            filtered_df = filtered_df[filtered_df['Category'].str.lower() >= category.lower()]

        if min_amount is not None:
            filtered_df = filtered_df[filtered_df['Amount'] >= min_amount ]

            print("\n ====== Filterd Result ======")
            if filtered_df.empty:
                print("No maching expense found .")

            else:
                print(filtered_df.to_string(index = False))

    def generate_report(self):

        if self.df.empty:
            print("no Data avilable to plot charts!")
            return

        sns.set_theme(style="whitegrid")
        fig.axes = plt.subplots(2,2,figsize=(12,10))
        fig.suptitle('Smart Expense Tracker Analytics',fontsize = 18)

        # 1. BAr Chart :Total expense by category

        cat_data = self.df.groupby('Category')['Amount'].sum().reset_index()
        sns.barplot(data = cat_data , x = 'category' , y = 'Amount' , ax = axes[0,0], palette='Blues_d')
        axes[0,0].set_title('Total Expense by Category')
        axes[0,0].set_ylabel('Amount')


        # 2. Line Chart : Spending Trends over Time

        time_data = self.df.groupby(Date)['Amount'].sum().reset_index
        sns.lineplot(date = time_data, x = 'Date' , y = 'Amount', ax = axes[0,1],marker = 'o' , color = 'red')
        axes[0,1].set_title('Spending Trends Over Time')
        axes[0,1].tick_params(axis = 'x' ,rotation = 45)


        # 3.Pie Chart : Proportional Spending

        category_totals = self.df.groupby('category')['Amount'].sum()
        axes[1,0].pie(category_totals,labels = category_totals.index,autopct = '%1.1f%%',startangle = 90)
        axes[1,0].set_title('Spending Disribution by Category')

        # 4. Histogram : Frequency of Expense Amount

        sns.histplot(self.df['Amount'],kde=True,ax=axes[1,1],color = 'purpule',bins=5)
        axes[1,1].set_title(Frequency of Expense Amounts)

        plt.tight_layout()
        plt.show


# Main Workflow

if _name_ == "_main_":
    tracker = Expensetracker('Expense.csv')

    while True:
        print("\n ======= SMART EXPENSE TRACKER =======")
        print("1. Add New Exense")
        print("2. View Expense summary ")
        print("3. Filter Expense")
        print("4. Generate Visual Charts")
        print("5. Exit")

        Choice = input("Enter your choice :")

        if choice == 1:

            date = input("Enter Date (YYYY-MM-DD):")
            amount = input("Enter Amount :")
            category = input("Enter category(Food , Transport  , Utilities, Entertainment , Shopping, Other ) ")
            desc = input("Enter Description :")

            tracker.add_expense(date,amount,category,desc)

        elif Choice == 2:

            tracker.get_summary()

        elif Choice == 3:

            cat = input("Enter category to filter (or press enter to skip) :")
            amt = input("Enter minimum amount ( or press enter to skip ) :")
            amt_val = float(amt) if amt else None


            tracker.filter_expense(category = cat if cat else None , min_amount = amt_val)

        elif Choice == 4:

            tracker.generate_report()

        elif Choice == 5:

            print("Exiting application .")
            print("Good bye !!")

            break

        else:

            print("Invalid choice . ")
            print("Please enter 1 to 5!!")

            

        




    



