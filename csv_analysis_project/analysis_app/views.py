import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from .forms import UploadFileForm
import os

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            
            # Save file temporarily
            file_path = 'uploaded_file.csv'
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
                    
            # Read and process the CSV file
            data = pd.read_csv(file_path)
            
            # Basic analysis
            first_rows = data.head()
            description = data.describe()
            missing_values = data.isnull().sum()

            # Plotting a histogram of numerical columns
            plt.figure(figsize=(6, 4))
            for col in data.select_dtypes(include='number').columns:
                plt.figure()
                sns.histplot(data[col], kde=True)
                plt.title(f'Histogram of {col}')
                static_dir = os.path.join(os.getcwd(), 'static') 
                if not os.path.exists(static_dir):
                    os.makedirs(static_dir)
                plt.savefig(os.path.join(static_dir, f"{col}_histogram.png"))
            return render(request, 'results.html', {
                'first_rows': first_rows.to_html(),
                'description': description.to_html(),
                'missing_values': missing_values.to_frame().to_html(),
                'columns': data.columns,
                'file_path': file_path
            })
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})
