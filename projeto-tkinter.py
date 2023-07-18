import customtkinter
import json
import pymongo
import tkinter.messagebox as tkMessageBox

myclient = pymongo.MongoClient("mongodb://localhost:27017/") # string de conexao para o mongodb


customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class ScrollableDataFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, data):
        super().__init__(master)
        
        # Configure all columns to have the same weight and size
        # num_columns = len(data[0])
        # for column in range(num_columns):
            # self.grid_columnconfigure(column, weight=1, uniform="uniform_key")
        
        count = 0
        for field1 in data[0]:
            self.title = customtkinter.CTkLabel(self, text=field1, fg_color="#3b3b3b", corner_radius=6)
            self.title.configure(font=("Arial", 22))
            self.title.grid(row=0, column=count, padx=5, pady=5, sticky="nsew")
            count += 1
            
        rowCounter = 1
        conta = 0
        for documents in data:
            columnCounter = 0
            
            for document in documents:
                self.documentData = customtkinter.CTkLabel(self, text=documents[document], corner_radius=6)
                self.documentData.configure(font=("Arial", 22))
                self.documentData.grid(row=rowCounter, column=columnCounter, padx=5, pady=5, sticky="nsew")
                columnCounter += 1
                conta += 1
            rowCounter += 1

        

        
class ViewsFrame(customtkinter.CTkFrame): #ver documentos
    def __init__(self, master):
        super().__init__(master)
        try:
            workingDatabase = MenuFrame.optionmenu_var.get()
            workingCollection = MenuFrame.optionmenu_varCol.get()
            
            print(workingCollection, workingDatabase)
            
            mydb = myclient[workingDatabase]
            mycol = mydb[workingCollection]
            
        except Exception as e:
            tkMessageBox.showinfo("Erro!", "Selecione uma base de dados primeiro")
            raise ValueError("No db selected")
    

        data = mycol.find()
        arr = []
        for dat in data:
            arr.append(dat)
        
        print(arr)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.title = "Ver Documentos"
        
        self.title = customtkinter.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.configure(font=("Arial", 30))
        
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.dataList = ScrollableDataFrame(self, arr)
        self.dataList.grid(row=1, column=0, padx="5", pady="5", sticky="nsew")

        

class MenuFrame(customtkinter.CTkFrame):
    
    optionmenu_var = None
    
    def getDatabases(self):
        dbs = []
        
        for db in myclient.list_databases():
            dbs.append(db['name'])
            
            
        labelCol = customtkinter.CTkLabel(self, text="Collection:")
        labelCol.grid(row=2, column=0, padx=20, pady=0, sticky="ew")
        MenuFrame.optionmenu_var = customtkinter.StringVar(value="Select DB")
        MenuFrame.optionmenu = customtkinter.CTkOptionMenu(self,values=dbs,
                                                command=self.getCollection,
                                                variable=MenuFrame.optionmenu_var)

        MenuFrame.optionmenu.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="ew")
        
        return dbs
    
    def getCollection(self, database):
        cols = []
        
        database = MenuFrame.optionmenu_var.get()
        
        mydb = myclient[database]
        
        for collection in mydb.list_collection_names():
            cols.append(collection)
            
        labelCol = customtkinter.CTkLabel(self, text="Collection:")
        labelCol.grid(row=2, column=0, padx=20, pady=0, sticky="ew")

        MenuFrame.optionmenu_varCol = customtkinter.StringVar(value=cols[0])
        MenuFrame.optionmenuCol = customtkinter.CTkOptionMenu(self,values=cols,
                                                variable=MenuFrame.optionmenu_varCol)
        MenuFrame.optionmenuCol.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
    
    def __init__(self, master, title):
        super().__init__(master)

        self.title = title

        dbs = self.getDatabases()
        
        labelDB = customtkinter.CTkLabel(self, text="Database:")
        labelDB.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

    
        
        self.button2 = customtkinter.CTkButton(self, text="Ver Documentos", command=master.changeFrame2)
        self.button2.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        self.button3 = customtkinter.CTkButton(self, text="Adicionar Documento", command=master.changeFrame2)
        self.button3.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        
        self.button3 = customtkinter.CTkButton(self, text="Remover Documento", command=master.changeFrame2)
        self.button3.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        



class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title("Projeto MongoDB (BDNoSQL)") 
        self.geometry("1280x720")
        
        self.MenuFrame = MenuFrame(self, "Menu")
        self.MenuFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
    def changeFrame2(self):
        self.ViewsFrame = ViewsFrame(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        

app = App()
app.mainloop()