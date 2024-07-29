from django.shortcuts import render, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
# Create your views here.
def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():
        if response.method=="POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    
                    item.save()

            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                
                if len(txt)>2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("Invalid")
   # items = ls.item_set.get(id=1)
        return render(response, "list.html", {"ls": ls} )#{{}} in html is a variable, {} is a block
    return render(response, "view.html", {})

def create(request):
    if request.method=="POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"] 
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)
            
            return HttpResponseRedirect(f"/{t.id}")
            
    else:
        form = CreateNewList()
    
    return render(request, "create.html",  {"form": form})
    


def home(request):
    return render(request, "home.html")

def view(response):
    return render(response, "view.html", {})