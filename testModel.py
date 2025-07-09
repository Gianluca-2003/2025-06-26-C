from model.model import Model

myModel = Model()


myModel.buildGraph(2010,2016)


print(myModel.printGraph())


lista = myModel.get_info_comp()
for item in lista:
    print(item[1],'-->',item[0])
