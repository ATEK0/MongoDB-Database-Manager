import customtkinter
import tkinter as tk
import json
import pymongo
import tkinter.messagebox as tkMessageBox

myclient = pymongo.MongoClient("mongodb://localhost:27017/") # string de conexao para o mongodb

import os
import sys
import time
    
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# class ScrollableDataFrame(customtkinter.CTkScrollableFrame):
#     def __init__(self, master, data):
#         super().__init__(master)
        
#         # Find all unique fields from the data
#         fieldsName = set()
#         for documents in data:
#             fieldsName.update(documents.keys())

#         rowCounter = 1
#         conta = 0
#         count = 0
        
#         for document in fieldsName:
#             self.title = customtkinter.CTkLabel(self, text=document, fg_color="#3b3b3b", corner_radius=6)
#             self.title.configure(font=("Arial", 12))
#             self.title.grid(row=0, column=count, padx=5, pady=5, sticky="nsew")
#             count += 1

#         for documents in data:
#             columnCounter = 0
#             for field in fieldsName:
#                 self.documentData = customtkinter.CTkLabel(self, text=documents.get(field, ''), corner_radius=6)
#                 self.documentData.configure(font=("Arial", 12))
#                 self.documentData.grid(row=rowCounter, column=columnCounter, padx=5, pady=5, sticky="nsew")
#                 columnCounter += 1
#                 conta += 1
#             rowCounter += 1

class ScrollableDataFrame(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)

        # Find all unique fields from the data
        fieldsName = set()
        for documents in data:
            fieldsName.update(documents.keys())

        # Move 'id' field to the beginning of the set
        fieldsName.discard('_id')
        fieldsName = ['_id'] + sorted(fieldsName)

        rowCounter = 1
        conta = 0
        count = 0

        canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create horizontal scrollbar
        x_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.configure(xscrollcommand=x_scrollbar.set)

        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)

        for document in fieldsName:
            title = tk.Label(content_frame, text=document, fg="#3b3b3b", font=("Arial", 12))
            title.grid(row=0, column=count, padx=5, pady=5, sticky="nsew")
            count += 1

        for documents in data:
            columnCounter = 0
            for field in fieldsName:
                documentData = tk.Label(content_frame, text=documents.get(field, ''), font=("Arial", 12))
                documentData.grid(row=rowCounter, column=columnCounter, padx=5, pady=5, sticky="nsew")
                columnCounter += 1
                conta += 1
            rowCounter += 1

        # Update the scroll region to include the new content
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))



        
class ViewsFrameAddCollection(customtkinter.CTkFrame): #ver documentos
    def __init__(self, master):
        super().__init__(master)
        try:
            workingDatabase = MenuFrame.optionmenu_var.get()
            mydb = myclient[workingDatabase]

        except Exception as e:
            tkMessageBox.showinfo("Erro!", "Selecione uma base de dados primeiro")
            raise ValueError("No db selected")
        
        self.title = "Adicionar Collection"
        
        self.title = customtkinter.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.configure(font=("Arial", 30))
        
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    
        self.collection_name_label = customtkinter.CTkLabel(self, text="Nome da Colletion:")
        self.collection_name_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.collection_name_entry = customtkinter.CTkEntry(self, width=250)
        self.collection_name_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")

        self.create_collection_button = customtkinter.CTkButton(self, text="Criar Collection", command=self.create_collection)
        self.create_collection_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def create_collection(self):
        try:
            workingDatabase = MenuFrame.optionmenu_var.get()
            collection_name = self.collection_name_entry.get()

            if not collection_name:
                tkMessageBox.showinfo("Erro!", "Insira um nome para a collection.")
                return

            mydb = myclient[workingDatabase]
            mycol = mydb[collection_name]

            mycol.insert_one({"_": "_"})

            tkMessageBox.showinfo("Sucesso!", f"Colletion '{collection_name}' criada com sucesso.")
            
            self.collection_name_entry.delete(0, len(self.collection_name_entry.get()))
            
            self.master.MenuFrame.getCollections(workingDatabase)

        except Exception as e:
            tkMessageBox.showinfo("Erro!", str(e))


class ViewsFrameDeleteCollection(customtkinter.CTkFrame): #ver documentos
    def __init__(self, master):
        super().__init__(master)
        try:
            workingDatabase = MenuFrame.optionmenu_var.get()
            workingCollection = MenuFrame.optionmenu_varCol.get()
            
            print(workingCollection, workingDatabase)
            
            mydb = myclient[workingDatabase]
            
        except Exception as e:
            tkMessageBox.showinfo("Erro!", "Selecione uma base de dados primeiro")
            raise ValueError("No db selected")
    
        
        self.title = "Apagar Collection"
        
        self.title = customtkinter.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.configure(font=("Arial", 30))
        
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.collection_name_label = customtkinter.CTkLabel(self, text="Nome da Colletion:")
        self.collection_name_label.grid(row=1, column=0, padx=20, pady=(10,0), sticky="w")

        self.collection_name_entry = customtkinter.CTkEntry(self, width=250)
        self.collection_name_entry.grid(row=2, column=0, padx=20, pady=(0,10), sticky="w")
        
        self.delete_collection_button = customtkinter.CTkButton(self, text="Apagar Collection", command=self.deleteColection)
        self.delete_collection_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        
    def deleteColection(self):
        try:
            workingDatabase = MenuFrame.optionmenu_var.get()
            collection_name = self.collection_name_entry.get()

            if not collection_name:
                tkMessageBox.showinfo("Erro!", "Insira o nome da collection.")
                return

            mydb = myclient[workingDatabase]
            mycol = mydb[collection_name]

            mycol.drop()

            tkMessageBox.showinfo("Sucesso!", f"Colletion '{collection_name}' apagada com sucesso.")
            
            self.collection_name_entry.delete(0, len(collection_name))
            
            self.master.MenuFrame.getCollections(workingDatabase)

        except Exception as e:
            tkMessageBox.showinfo("Erro!", str(e))
        
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
        

class ViewsFrameAdd(customtkinter.CTkScrollableFrame): #Add Documents
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

        self.row = 4
        
        self.title = "Adicionar Documentos"
        
        self.title = customtkinter.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.configure(font=("Arial", 30))
        
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.add_fieldBTN= customtkinter.CTkButton(self, text="Adicionar Campo", width=350, command=self.addField)
        self.add_fieldBTN.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.insertDocumentBTN = customtkinter.CTkButton(self, text="Inserir Dados", width=350, command=self.get_entry_values)
        self.insertDocumentBTN.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        
        self.collection_name_label = customtkinter.CTkLabel(self, text="Nome do campo:")
        self.collection_name_label.grid(row=2, column=0, padx=20, pady=(10,0), sticky="w")
        self.collection_name_label = customtkinter.CTkLabel(self, text="Valor do campo:")
        self.collection_name_label.grid(row=2, column=1, padx=20, pady=(10,0), sticky="w")

        self.collection_name_entry = customtkinter.CTkEntry(self, width=250)
        self.collection_name_entry.grid(row=3, column=0, padx=20, pady=(0,10), sticky="w")
        self.collection_name_entry = customtkinter.CTkEntry(self, width=250)
        self.collection_name_entry.grid(row=3, column=1, padx=20, pady=(0,10), sticky="w")
        
        
    def addField(self):
        self.collection_name_entry = customtkinter.CTkEntry(self, width=250)
        self.collection_name_entry.grid(row=self.row, column=0, padx=20, pady=(0,10), sticky="w")
        self.collection_name_entry = customtkinter.CTkEntry(self, width=250)
        self.collection_name_entry.grid(row=self.row, column=1, padx=20, pady=(0,10), sticky="w")
        
        self.row += 1
    
    def insertData(self, valores):
        workingDatabase = MenuFrame.optionmenu_var.get()
        workingCollection = MenuFrame.optionmenu_varCol.get()
        
        print(workingCollection, workingDatabase)
        
        mydb = myclient[workingDatabase]
        mycol = mydb[workingCollection]
        
        mycol.delete_many({"_": "_"})
        
        counter = 1
        pre = 0
        for entry, value in valores.items():
            print(counter)
            if counter == 1:
                pre = value
                counter += 1
            elif counter == 2:
                if pre == "" and value == "":
                    tkMessageBox.showinfo("Erro!", "Documentos vazios não serão inseridos")    
                else:
                    mycol.insert_one({f"{pre}": f"{value}"})
                    counter = 1 
            print(f"pre {pre}, valor atual {value}")
    
    def get_entry_values(self):
        entry_values = {}
        for widget in self.winfo_children():
            if isinstance(widget, customtkinter.CTkEntry):
                entry_values[widget] = widget.get()
                        
        self.insertData(entry_values)
        
        
        

        

class ViewsFrameDelete(customtkinter.CTkFrame): #Delete Documents
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
        
        
        
class ViewsFrameGerirDB(customtkinter.CTkFrame): #Gerir Base de Dados
    
    def createDatabase(self):
        try:
            database = self.DatabaseName.get()
            
            db = myclient[database]
            
            collection = db["CreationCollection"]
            
            result = collection.insert_one({"_": "_"})

            
            tkMessageBox.showinfo("Sucesso!", f"Base de dados {database} criada com sucesso")
            self.master.MenuFrame.getDatabases()
            
        except Exception as e:
            tkMessageBox.showinfo("Erro!", e)
            
    def deleteDatabase(self):
    
        try:
            database = self.DatabaseName.get()
            
            myclient.drop_database(database)
            
            tkMessageBox.showinfo("Sucesso!", f"Base de dados {database} apagada com sucesso")
            self.master.MenuFrame.getDatabases()
            
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
        self.AddDB = customtkinter.CTkButton(self, text="Add Database", width=250, corner_radius=6, command=self.createDatabase)
        self.AddDB.grid(row=4, column=0,columnspan=2, padx=12, pady=5, sticky="nw")
        
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
        self.DatabaseNameLabel.configure(font=("Arial", 20))

        self.DatabaseName = customtkinter.CTkEntry(self, width=250)
        self.DatabaseName.grid(row=4, column=0, padx=12, pady=5, sticky="nw")
        self.AddDB = customtkinter.CTkButton(self, text="Delete Database", width=250, corner_radius=6, command=self.deleteDatabase)
        self.AddDB.grid(row=5, column=0, padx=12, pady=5, sticky="nw")
        self.buttonDelDB.configure(font=("Arial", 20))    
        self.buttonDelDB.grid(row=2, column=0, padx=12, pady=5, sticky="nw")
        

class ViewsFrameSearch(customtkinter.CTkFrame): #Perquisar
    def __init__(self, master):
        super().__init__(master)
        try:
            workingDatabase = MenuFrame.optionmenu_var.get()
            workingCollection = MenuFrame.optionmenu_varCol.get()
            
            print(workingCollection, workingDatabase)
            
            mydb = myclient[workingDatabase]
            
        except Exception as e:
            tkMessageBox.showinfo("Erro!", "Selecione uma base de dados primeiro")
            raise ValueError("No db selected")
    
        
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.title = "Pesquisar"
        
        self.title = customtkinter.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.configure(font=("Arial", 30))
        
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        

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
                                                command=self.getCollections,
                                                variable=MenuFrame.optionmenu_var)

        MenuFrame.optionmenu.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="ew")
        
        return dbs
    
    def getCollections(self, database):
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
        
        self.buttonAddCol = customtkinter.CTkButton(self, text="Adicionar Collection", command=master.changeFrameAddCol)
        self.buttonAddCol.grid(row=8, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonDeleteCol = customtkinter.CTkButton(self, text="Remover Collection", command=master.changeFrameDelCol)
        self.buttonDeleteCol.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonAddDocs = customtkinter.CTkButton(self, text="Adicionar Documento", command=master.changeFrameAddDoc)
        self.buttonAddDocs.grid(row=10, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonDeleteDocs = customtkinter.CTkButton(self, text="Remover Documento", command=master.changeFrameDeleteDoc)
        self.buttonDeleteDocs.grid(row=11, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonSearch = customtkinter.CTkButton(self, text="Pesquisar", command=master.changeFrameSearch)
        self.buttonSearch.grid(row=12, column=0, padx=20, pady=10, sticky="w")
        
        self.buttonExit = customtkinter.CTkButton(self, text="Sair", command=master.sair)
        self.buttonExit.grid(row=13, column=0, padx=20, pady=10, sticky="w")
        



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
        
    def changeFrameAddCol(self):
        self.ViewsFrame = ViewsFrameAddCollection(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nsew")
        
    def changeFrameDelCol(self):
        self.ViewsFrame = ViewsFrameDeleteCollection(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
    def changeFrameAddDoc(self):
        self.ViewsFrame = ViewsFrameAdd(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
    def changeFrameDeleteDoc(self):
        self.ViewsFrame = ViewsFrameDelete(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
    def changeFrameSearch(self):
        self.ViewsFrame = ViewsFrameSearch(self)
        self.ViewsFrame.grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        
    def sair(self):
        quit()

app = App()
app.mainloop()