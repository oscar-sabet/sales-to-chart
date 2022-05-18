import tkinter as tk
# Used for styling the GUI
from tkinter import ttk, filedialog
import os
import csv
import matplotlib.pyplot as plt

from decimal import Decimal
# from tkinter.scrolledtext import ScrolledText


import tkinter as tk

current_working_dir = ""  # os.getcwd()


class ExpensesApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.wm_title("Expenses App")
        self.iconbitmap(r'document_graph.ico')

        self.current_working_folder = ""

        self.totals = []
        # Contains working dir-text box / and select dir, create chart-buttons
        self.dir_label = ttk.LabelFrame(
            self,
            text='Current Folder'
        )

        self.dir_label.grid(
            column=0,
            row=0,
            padx=5,
            pady=5,
        )

        self.working_dir = tk.Text(
            self.dir_label,
            height=1,
            width=50,
            relief='solid',
            wrap='none',
        )

        self.working_dir.insert('1.0', self.current_working_folder)

        self.working_dir.pack(
            padx=5,
            pady=5,
            anchor='w',
            side='left'
        )

        self.create_chart = ttk.Button(
            self.dir_label,
            text="Create Chart",
            command=lambda: self.draw_graph(
                self.get_total(
                    self.load_csv(
                        self.current_working_folder)))
        )
        self.create_chart.pack(
            # anchor='e',
            side='right',
            padx=5,
            pady=5
        )
        self.select_dir = ttk.Button(
            self.dir_label,
            text="Select dir",
            command=lambda: self.new_dir()
        )
        self.select_dir.pack(
            # anchor='e',
            side='right',
            padx=5,
            pady=5
        )

    @classmethod
    def load_csv(self, path):
        """opens CSV files and loads data into a dictionary

        Args:
            path (Str): directory path of CSV files to load

        Returns:
            Dict: Dictionary of data loaded from CSV files
        """
        expenses = {}
        # checks if dir is empty or bool
        if isinstance(path, bool) or path == '':
            print("No directory passed")
            return False

        files = os.listdir(path)

        # finds CSV files in dir
        files = [x for x in files if ".csv" in x]
        years = []

        for x in files:
            # creates absolute path to file
            f = path + r"/" + x

            # removes file extention & uses filename as the year
            year = x.replace(".csv", "")
            years.append(year)
            expenses[year] = {}
            with open(f, "r", encoding='utf-8-sig') as file:
                csvreader = csv.reader(file)

                # skips the header
                header = [next(csvreader)]

                for row in csvreader:
                    money = row[1].replace("£", "")
                    money = money.replace(",", "")
                    expenses[year][row[0]] = Decimal(money)
        return expenses

    @classmethod
    def get_total(cls, expenses, choice='totals'):
        """Takes expenses dictionary and returns the data seperated with the totals

        Args:
            expenses (Dict): The expenses loaded from 
            choice (str, optional): returns year & totals if 'totals' passed, returns all 
            data if 'all' passed. Defaults to 'totals'.

        Returns:
            years, months, cost, totals: returns seperated values & totals
        """
        years = []
        months = []
        cost = []
        totals = []
        temp = []
        temp2 = []
        sum_month = 0

        if isinstance(expenses, bool):
            print("Error: func get_total-dict not passed")
            return False

        for year in expenses:
            years.append(year)

            temp = []
            sum_month = 0
            temp2 = []
            for month in expenses[year]:
                temp.append(month)

                sum_month += expenses[year][month]
                temp2.append(expenses[year][month])
            cost.append(temp2)
            months.append(temp)

            totals.append(sum_month)

        if choice == 'totals':
            return (years, totals)
        elif choice == 'all':
            return years, months, cost, totals

    def new_dir(self):
        """Gets new directory from user and updates UI
        """
        self.working_dir.delete('1.0', 'end')
        cwd = filedialog.askdirectory()

        # if user closes filedialog selects current dir
        if cwd == '':
            self.current_working_folder = os.getcwd()
            self.working_dir.insert("1.0", os.getcwd())
        else:
            self.current_working_folder = cwd
            self.working_dir.insert("1.0", cwd)

        temp = self.load_csv(self.current_working_folder)

        if isinstance(temp, bool):
            print("Error: No CSV files Found")

            self.totals_frame.grid_forget()

            return False
        else:
            try:
                print(type(self.totals_frame))
                self.totals_frame.grid_forget()
            except:
                print("no totals_frame loaded")

            try:
                self.error_msg.grid_forget()
            except:
                print("no error_msg loaded")

            years, months, cost, total = self.get_total(temp, 'all')
            self.load_data_into_ui(years, months, cost, total)

    def load_data_into_ui(self, years, months, cost, total):
        """creates UI elements and loads data into it

        Args:
            years (list): Split from CSV data
            months (list): Split from CSV data
            cost (list): Split from CSV data
            total (list): Split from CSV data
        """
        temp = ""
        self.totals = []
        self.totals_frame = ttk.LabelFrame(
            self,
            text="Loaded Data"
        )

        self.totals_frame.grid(
            padx=5,
            pady=5,
        )

        # if no loaded data gives error msg
        if len(years) == 0:
            self.error_msg = ttk.Label(
                text="Error: No CSV files found.\n Select another folder",
                foreground="red"
            )

            self.error_msg.grid(
                padx=10,
                pady=10,
            )

        else:
            for i in range(len(years)):
                self.totals.append([i, i])

                # creates label frame for each year
                self.totals[i][0] = ttk.LabelFrame(
                    self.totals_frame,
                    text=years[i]
                )

                self.totals[i][0].grid(
                    column=i,
                    row=1,
                    padx=5,
                    pady=5,
                )

                # creates total at top of list
                temp = "Total"
                temp = f"{temp:9}£{total[i]:,}\n\n"

                # Adds data to rest of list
                for k in range(len(months[i])):
                    money = f"£{cost[i][k]:,.2f}"
                    temp += f"{months[i][k]:9} {money:>9}\n"

                self.totals[i][1] = tk.Text(
                    self.totals[i][0],
                    height=14,
                    width=19,
                    relief='solid',
                )

                self.totals[i][1].pack(
                    padx=5,
                    pady=5,
                )
                self.totals[i][1].insert('1.0', temp)

    def draw_graph(self, xy):
        """takes x and y axis data and creates a horizontal graph

        Args:
            xy (List): list containing x & y axis data
        """
        colors = ['green', 'blue', 'purple', 'brown', 'teal']
        fig = plt.figure(figsize=(10, 5))
        plt.barh(
            xy[0], xy[1],
            color=colors,
            edgecolor="black",
            linewidth=2
        )

        plt.title('Total Expenses by Year')
        plt.xlabel('Total Expenses')
        plt.ylabel('Year')
        plt.show()


def main():
    """mainloop for the program
    """
    app = ExpensesApp()
    # app = ExpensesApp(root)
    app.new_dir()
    app.mainloop()


if __name__ == '__main__':
    main()
