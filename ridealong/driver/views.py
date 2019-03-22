from django.shortcuts import render
from django.shortcuts import redirect
from .models import DriveRequest, Car
from accounts.models import Profile
from . import views

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    print (request.method)
    if request.method == "POST":
        print(request.POST['departLoc'])
        print(request.POST['arrivalLoc'])
        print(request.POST['pickupTime'])
        print(request.POST['dropTime'])
        print(request.POST['seats'])
        print(request.POST['baggage'])
        departLoc = request.POST['departLoc']
        arrivalLoc = request.POST['arrivalLoc']
        pickupTime = request.POST['pickupTime']
        dropTime = request.POST['dropTime']
        numOfSeats = request.POST['seats']
        numOfBaggage = request.POST['baggage']
        if departLoc and arrivalLoc and pickupTime and dropTime and numOfSeats and numOfBaggage:
            driveRequest_instance = DriveRequest.objects.create(
                departLoc = request.POST['departLoc'],
                arrivalLoc = request.POST['arrivalLoc'],
                pickupTime = request.POST['pickupTime'],
                dropTime = request.POST['dropTime'],
                numOfSeats = request.POST['seats'],
                numOfBaggage = request.POST['baggage'],
            )
            driveRequest_instance.save()
        make = request.POST['carMake']
        model = request.POST['carModel']
        year = request.POST['carYear']

        if make and model and year:
            car = Car.objects.create(
                Make = make,
                Model = model,
                Year = year
            )
            car.save()
            driveRequest_instance.Car = car
            driveRequest_instance.save()
        """
        deleteID = request.POST['deleteID']
        editID = request.POST['editID']
        editField = request.POST['editField']
        editVal = request.POST['editVal']
        if deleteID:
            print("delete record here")
        if editID and editField and editVal:
            print("edit record here")
        """
        print(request.user)
        driveRequest_instance.Rider = request.user

        driveRequest_instance.save()

    driveRequests = DriveRequest.objects.all()
    print("driveRequests:")
    print(driveRequests)
    return render(request,"driver_page.html",{'isIndex':True,'driveRequests':driveRequests})

def driverSearch(request):
    #ex. query http://localhost:8000/driver/search?searchText=West&filter=location
    #filter options: location,date,price,luggage,passengershttp://localhost:8000/driver/search?Filter=Price
    if request.method == "GET":
        if request.GET['filter'] == 'location':
            searchResult = DriveRequest.objects.filter(departLoc__search=request.GET['searchText'])

    return render(request,"driver_page.html",{'isIndex':False,'searchResult':searchResult})

def ridepopup(request):
    return render(request,'ridePopup.html')

def profile(request):
    if request.user.is_authenticated:
        print("IN")
        username = request.user.email
        #print(userName)
        profilePage = Profile.objects.filter(ContactEmail=username)
        return render(request,"profile.html",{'profilePage':profilePage})
    else:
        return render(request, "profile.html")
    # return render(request, 'profile.html')

