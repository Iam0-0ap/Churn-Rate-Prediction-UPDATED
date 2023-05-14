from inspect import Parameter
from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import clear_script_prefix
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import joblib 
import pandas as pd 


def home(request):
    return render(request, 'users/home.html')


def discover(request):
    return render(request, 'users/discover.html')

def about(request):
    return render(request, 'users/aboutus.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

@login_required()
def churn(request):
    return render(request, 'users/churn.html')

# @login_required()
# def churn(request):
#     return render(request, 'users/result.html')

# def result(request):
#     cls= joblib.load('final_LR_model.sav')
#     lis = dict()

#     lis['Dependents'] = [request.POST.get('Dependents')]
#     lis['tenure'] = [request.POST.get('tenure')]
#     lis['PhoneService'] = [request.POST.get('PhoneService')]
#     lis['MultipleLines'] = [request.POST.get('MultipleLines')]
#     lis['InternetService'] = [request.POST.get('InternetService')]
#     lis['OnlineSecurity'] = [request.POST.get('OnlineSecurity')]
#     lis['StreamingServices'] = [request.POST.get('StreamingServices')]
#     lis['OnlineBackup'] = [request.POST.get('OnlineBackup')]
#     lis['DeviceProtection'] = [request.POST.get('DeviceProtection')]
#     lis['TechSupport'] = [request.POST.get('TechSupport')]
#     lis['Contract'] = [request.POST.get('Contract')]
#     lis['PaperlessBilling'] = [request.POST.get('PaperlessBilling')]
#     lis['PaymentMethod'] = [request.POST.get('PaymentMethod')]
#     lis['MonthlyCharges'] = [request.POST.get('MonthlyCharges')]
#     lis['Age'] = [request.POST.get('Age')]
#     lis['Married'] = [request.POST.get('Married')]
#     lis['Number of Referrals'] = [request.POST.get('Number of Referrals')]
#     lis['Offer'] = [request.POST.get('Offer')]
#     lis['Avg Monthly GB Download'] = [request.POST.get('Avg Monthly GB Download')]
#     lis['Premium Tech Support'] = [request.POST.get('Premium Tech Support')]
#     lis['Unlimited Data'] = [request.POST.get('Unlimited Data')]
#     print(lis)

#     data_df = pd.DataFrame(lis)
#     ans= cls.predict(data_df)
#     probs= cls.predict_proba(data_df)
#     return render(request,"users/result.html")

def result(request):
    model = joblib.load('final_SGD_model.sav')
    
    parameters = dict()
    columns = list()
    data = list()


    parameters['Married'] = request.POST.get('Married')
    parameters['Dependents'] = request.POST.get('Dependents')
    parameters['tenure'] = int(request.POST.get('tenure'))
    parameters['PhoneService'] = request.POST.get('PhoneService')
    parameters['MultipleLines'] = request.POST.get('MultipleLines')
    parameters['InternetService'] = request.POST.get('InternetService')
    parameters['OnlineSecurity'] = request.POST.get('OnlineSecurity')
    parameters['OnlineBackup'] = request.POST.get('OnlineBackup')
    parameters['DeviceProtection'] = request.POST.get('DeviceProtection')
    parameters['TechSupport'] = request.POST.get('TechSupport')
    parameters['Contract'] = request.POST.get('Contract')
    parameters['PaperlessBilling'] = request.POST.get('PaperlessBilling')
    parameters['PaymentMethod'] = request.POST.get('PaymentMethod')
    parameters['MonthlyCharges'] = int(request.POST.get('MonthlyCharges'))
    parameters['StreamingServices'] = request.POST.get('StreamingServices')
    parameters['Age'] = int(request.POST.get('Age'))
    parameters['Number of Referrals'] = int(request.POST.get('Number of Referrals'))
    # parameters['Offer'] =request.POST.get('Offer')
    parameters['Avg Monthly GB Download'] = int(request.POST.get('Avg Monthly GB Download'))
    parameters['Premium Tech Support'] = request.POST.get('Premium Tech Support')
    parameters['Unlimited Data'] = request.POST.get('Unlimited Data')


    for key, item in parameters.items():
        columns.append(key)
        data.append(item)

    dummy = pd.DataFrame([data], columns = columns)
    prediction = model.predict(dummy)
    prediction_prob = model.predict_proba(dummy)
    print(prediction[0])

    to_return = {
        'predicted_class' : prediction[0],
        'churn_prob' : round(prediction_prob[0][1], 4) * 100
    }

    return render(request, 'users/result.html', to_return)
