import customtkinter as ctk
import sqlite3
import datetime

# Converts database into list
def fetch_db(db):
  cursor = db.cursor()
  cursor.execute("SELECT * FROM data;")
  data = cursor.fetchall()
  db.close()
  return data

# Window
class Root(ctk.CTk):
  def __init__(self):
    super().__init__()

    # Window settings
    self.title("Expense Manager")
    self.winwidth = 1920
    self.winheight = 1080
    self.geometry(f"1920x1080+{(self.winfo_screenwidth() - self.winwidth) // 2}+{(self.winfo_screenheight() - self.winheight) // 2}")
    self._set_appearance_mode("dark")

    self.analyticsFrame = Analytics(self, (self.winwidth // 2), self.winheight)
    self.listFrame = ExpenseList(self, (self.winwidth // 2), self.winheight)

    # Section configuration
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)
    self.analyticsFrame.grid(row=0, column=0)
    self.listFrame.grid(row=0, column=1)

    # Run window
    self.mainloop()

class Analytics(ctk.CTkFrame):
  def __init__(self, master, framewidth, frameheight):
    super().__init__(master, width=framewidth, height=frameheight)

    self.months = []
    for entry in data:
      if entry[0][0:2] not in self.months:
        self.months.append(entry[0][0:2])
    self.months.sort()
    self.years = []
    for entry in data:
      if entry[0][-4:] not in self.years:
        self.years.append(entry[0][-4:])

    self.monthVar = ctk.StringVar()
    self.yearVar = ctk.StringVar()
    monthSelect = ctk.CTkComboBox(master=self, values=self.months, variable=self.monthVar, command=self.update_month)
    yearSelect = ctk.CTkComboBox(master=self, values=self.years, variable=self.yearVar, command=self.update_year)

    monthSelect.pack()
    yearSelect.pack()

  def update_month(self, month):
    self.update_info(month, None)

  def update_year(self, year):
    self.update_info(None, year)

  def update_info(self, month, year):
    if month:
      print(month)
    elif year:
      print(year)
    # total = 0
    # for entry in data:
    #   if ((entry[0][0:2] == self.current_month()) and (entry[0][-4:] == self.current_year())):
    #     total += float(entry[1])
    # print(total)

    # spentString = f"Total Spent: {total}"
    # spentLabel = ctk.CTkLabel(self, text=spentString)
    # spentLabel.pack()

class ExpenseList(ctk.CTkScrollableFrame):
  def __init__(self, master, framewidth, frameheight):
    super().__init__(master, width=framewidth, height=frameheight)

    # Displays data content in grid
    col_order = [4, 1, 0]
    gridData = data
    gridData.insert(0, ("Date", "Cost", None, None, "Expense"))
    for rowIDX, row in enumerate(gridData):
      for colIDX, value in enumerate(row):
        if colIDX in col_order:
          entryLabel = ctk.CTkLabel(self, text=value)
          entryLabel.grid(row=rowIDX, column=col_order.index(colIDX))

if __name__ == "__main__":
  # Obtains database information
  global data
  db = sqlite3.connect("data.db")
  data = fetch_db(db)

  # Obtains current date
  date = datetime.date.today()
  global currentMonth
  global currentYear

  # Create window
  Root()

#   self.total_spend = self.get_total_spend()
#   self.total_spend = "{:,.2f}".format(round(self.total_spend, 2)).replace("-", "")
#   self.spend_string = f"Total Spending: {self.total_spend}"

#   self.total_add = self.get_total_add()
#   self.total_add = "{:,.2f}".format(round(self.total_add, 2))
#   self.add_string = f"Total Added: {self.total_add}"

#   spendLabel = ctk.CTkLabel(self, text=self.spend_string)
#   spendLabel.pack()
#   addLabel = ctk.CTkLabel(self, text=self.add_string)
#   addLabel.pack()

# def get_total_spend(self):
#   total = 0
#   for entry in data:
#     if (float(entry[1]) < 0):
#       total += float(entry[1])
#   return total

# def get_total_add(self):
#   total = 0
#   for entry in data:
#     if (float(entry[1]) > 0):
#       total += float(entry[1])
#   return total