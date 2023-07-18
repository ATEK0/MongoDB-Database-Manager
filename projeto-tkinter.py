import customtkinter
import json
import pymongo
import tkinter.messagebox as tkMessageBox

myclient = pymongo.MongoClient("mongodb://localhost:27017/") # string de conexao para o mongodb

import os
import sys
import time

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class ScrollableDataFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, data):
        super().__init__(master)
            
        rowCounter = 1
        conta = 0
        count = 0
        
        fieldsName = []
        for documents in data:
            columnCounter = 0

            for document in documents:
                if document not in fieldsName:
                    fieldsName.append(document)
                    self.title = customtkinter.CTkLabel(self, text=document, fg_color="#3b3b3b", corner_radius=6)
                    self.title.configure(font=("Arial", 12))
                    self.title.grid(row=0, column=count, padx=5, pady=5, sticky="nsew")
                    count += 1
                    
                self.documentData = customtkinter.CTkLabel(self, text=documents[document], corner_radius=6)
                self.documentData.configure(font=("Arial", 12))
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
        

class ViewsFrameAdd(customtkinter.CTkFrame): #ver documentos
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
        

class ViewsFrameDelete(customtkinter.CTkFrame): #ver documentos
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
        
class ViewsFrameGerirDB(customtkinter.CTkFrame): #ver documentos
    
    def createDatabase(self):
       
        try:
            database = self.DatabaseName.get()
            
            db = myclient[database]
            
            collection = db["CreationCollection"]
            
            result = collection.insert_one({"_": "_"})

            
            tkMessageBox.showinfo("Sucesso!", f"Base de dados {database} criada com sucesso")
            
            
        except Exception as e:
            tkMessageBox.showinfo("Erro!", e)

    
    def __init__(self, master):
        super().__init__(master)
        
        title = "Gerir Bases de Dados"
        
        title = customtkinter.CTkLabel(self, text=title, corner_radius=6)
        title.configure(font=("Arial", 30))
        
        title.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.buttonAddDB = customtkinter.CTkButton(self, text="Criar Base de Dados", width=250, corner_radius=6, command=self.addDatabaseMenu)
        self.buttonAddDB.configure(font=("Arial", 20))
        self.buttonAddDB.grid(row=1, column=0, padx=12, pady=5, sticky="nw")
        
        self.buttonDelDB = customtkinter.CTkButton(self, text="Apagar Base de Dados", width=250, corner_radius=6, command=self.deleteDatabaseMenu)
        self.buttonDelDB.configure(font=("Arial", 20))
        self.buttonDelDB.grid(row=2, column=0, padx=12, pady=5, sticky="nw")
        
    def addDatabaseMenu(self):
        try:
            self.DatabaseNameLabel.destroy()
            self.DatabaseName.destroy()
            self.AddDB.destroy()
            
        except Exception as e:
            ...
            
        self.DatabaseNameLabel = customtkinter.CTkLabel(self, text="Insert Database Name ")
        self.DatabaseNameLabel.grid(row=2, column=0, padx=12, pady=5, sticky="nw")
        self.DatabaseName = customtkinter.CTkEntry(self, width=250)
        self.DatabaseName.grid(row=3, column=0, padx=12, pady=5, sticky="nw")
        self.AddDB = customtkinter.CTkButton(self, text="Add Database", width=100, corner_radius=6, command=self.createDatabase)
        self.AddDB.configure(font=("Arial", 20))
        self.AddDB.grid(row=4, column=0, padx=12, pady=5, sticky="nw")
        
        self.buttonDelDB.configure(font=("Arial", 20))    
        self.buttonDelDB.grid(row=10, column=0, padx=12, pady=5, sticky="nw")
    
    def deleteDatabaseMenu(self):
        try:
            
            self.DatabaseNameLabel.destroy()
            
            self.DatabaseName.destroy()
            
            self.AddDB.destroy()
            
            
        except Exception as e:
            ...
            
        self.DatabaseNameLabel = customtkinter.CTkLabel(self, text="Delete Database Name ")
        self.DatabaseNameLabel.grid(row=3, column=0, padx=12, pady=5, sticky="nw")
        self.DatabaseName = customtkinter.CTkEntry(self, width=250)
        self.DatabaseName.grid(row=4, column=0, padx=12, pady=5, sticky="nw")
        self.AddDB = customtkinter.CTkButton(self, text="Delete Database", width=100, corner_radius=6, command=self.createDatabase)
        self.AddDB.configure(font=("Arial", 20))
        self.AddDB.grid(row=5, column=0, padx=12, pady=5, sticky="nw")
        self.buttonDelDB.configure(font=("Arial", 20))    
        self.buttonDelDB.grid(row=2, column=0, padx=12, pady=5, sticky="nw")
        


        

class MenuFrame(customtkinter.CTkFrame):
    
    optionmenu_var = None
    
    def getDatabases(self):
        print("cenas")
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

    
        self.buttonAddBD = customtkinter.CTkButton(self, text="Gerir Base de Dados", command=master.gerirDatabase)
        self.buttonAddBD.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonVerDocs = customtkinter.CTkButton(self, text="Ver Documentos", command=master.changeFrame2)
        self.buttonVerDocs.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonAddDocs = customtkinter.CTkButton(self, text="Adicionar Documento", command=master.changeFrameAdd)
        self.buttonAddDocs.grid(row=8, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonDeleteDocs = customtkinter.CTkButton(self, text="Remover Documento", command=master.changeFrameDelete)
        self.buttonDeleteDocs.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        



class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title("Projeto MongoDB (BDNoSQL)") 
        self.geometry("1280x720")
        
        
        
        self.MenuFrame = MenuFrame(self, "Menu")
        self.MenuFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        
    def gerirDatabase(self):
        self.ViewsFrame = ViewsFrameGerirDB(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
        
    def changeFrame2(self):
        self.ViewsFrame = ViewsFrame(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
    def changeFrameAdd(self):
        self.ViewsFrame = ViewsFrameAdd(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
    def changeFrameDelete(self):
        self.ViewsFrame = ViewsFrameDelete(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        

app = App()
app.mainloop()