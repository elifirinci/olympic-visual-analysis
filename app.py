import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import requests
from PIL import Image, ImageTk

address = 'https://www.bbc.com/sport/olympics/paris-2024/medals'
title = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
page = requests.get(address, headers=title)
soup = bs(page.content, "html.parser")

rows = soup.find_all("tr")

countries = []
gold_medals = []
silver_medals = []
bronze_medals = []
total_medals = []

for row in rows:
    cells = row.find_all("td")
    if len(cells) >= 6:
        spans = cells[1].find_all("span")
        if len(spans) == 2:
            country_name = spans[1].text.strip()
            countries.append(country_name)

        gold_medals.append(int(cells[2].text.strip()))
        silver_medals.append(int(cells[3].text.strip()))
        bronze_medals.append(int(cells[4].text.strip()))
        total_medals.append(int(cells[5].text.strip()))


class OlympicMedalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Olympic Medals")

        img = Image.open("C:/Users/eelif/Downloads/indir.png")
        img = ImageTk.PhotoImage(img)
        self.img = img
        self.image_label=tk.Label(root, image=img)
        self.image_label.pack(padx=10,pady=4)

        self.entry_link = tk.Entry(root, width="40")
        self.entry_link.pack(padx="20",pady="5")

        self.show_list_button = tk.Button(root, text="Show list", command=self.add_link)
        self.show_list_button.pack(padx="20",pady="7")

        self.country_listbox = tk.Listbox(root)
        self.country_listbox.pack(padx="20",pady="6")

        self.text_label = tk.Label(text="Click on a country to see detailed medals:")
        self.text_label.pack(padx="20", pady="3")

        self.show_chart_button = tk.Button(root, text="Show chart of selected country", command=self.show_chart)
        self.show_chart_button.pack(padx="20",pady="4")

        self.show_general_analytics_button = tk.Button(root, text="Show top 10 performing countries analytics", command=self.show_analytics)
        self.show_general_analytics_button.pack(padx="20",pady="7")

    def add_link(self):
        if self.entry_link.get()==address:
            self.country_listbox.delete(0, tk.END)
            for country in countries:
                self.country_listbox.insert(tk.END, country)

    def show_chart(self):
        selected_country_index = self.country_listbox.curselection()
        if not selected_country_index:
            messagebox.showwarning("No selection", "Please select a country")
            return

        selected_country_index = selected_country_index[0]
        selected_country = countries[selected_country_index]

        data = {
            "gold": gold_medals[selected_country_index],
            "silver": silver_medals[selected_country_index],
            "bronze": bronze_medals[selected_country_index]
        }
    
        medals = list(data.keys())
        counts = list(data.values())

        plt.bar(medals, counts, color=['gold', 'silver', 'brown'])
        plt.title(f"Medal Counts for {selected_country}")
        plt.ylabel("Count")
        plt.xlabel("Medal Type")

        plt.show()

    def show_analytics(self):
        sorted_indices = sorted(range(len(total_medals)), key=lambda i: total_medals[i], reverse=True)
        top_indices = sorted_indices[:10]

        top_countries = ([countries[i] for i in top_indices])
        top_gold = ([gold_medals[i] for i in top_indices])
        top_silver = ([silver_medals[i] for i in top_indices])
        top_bronze = ([bronze_medals[i] for i in top_indices])
        top_total = ([total_medals[i] for i in top_indices])

        plt.subplot(2, 2, 1)
        plt.pie(top_gold, labels=top_countries, autopct='%1.1f%%', startangle=90)
        plt.title("Gold Medals")

        plt.subplot(2, 2, 2)
        plt.pie(top_silver, labels=top_countries, autopct='%1.1f%%', startangle=90)
        plt.title("Silver Medals")

        plt.subplot(2, 2, 3)
        plt.pie(top_bronze, labels=top_countries, autopct='%1.1f%%', startangle=90)
        plt.title("Bronze Medals")

        plt.subplot(2, 2, 4)
        plt.plot(top_countries, top_total, marker='o', linestyle='-', color='blue')
        plt.title('Total Medals')
        plt.xlabel('Countries')
        plt.ylabel('Number of Medals')

        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = OlympicMedalGUI(root)
    root.mainloop()
