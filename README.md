
# Tread 

Online tool that help you to convert your webpages  seamlessly into a properly formatted epub which can be read across all your devices.
![image](https://github.com/user-attachments/assets/e3ab60af-d6e7-4d30-aed9-489ab5a2215b)



## 🌟 Features  
- Effortlessly convert blogs and webpages into ePub files.  
- API integration for automated workflows.  
- **Future Prospects**:  
  - 🚀 **Bionic Reading**: Read books faster with advanced visual enhancements.  
  - 📥 Download all books with a single click.  
  - 🎛️ Feature-rich dashboard for enhanced user experience.  

# 📚 Our Api Documentation

Convert a massive amount of webpages into **ePub** format seamlessly! Perfect for scraping entire blogging sites and transforming them into eBooks.  

---

# 📖 API Usage Instructions

## 🛠️ Step-by-Step Instructions

### 1. **Configure Your Account**  
   - Go to your **profile page** and enter all the required credentials.
   - Once your credentials are verified, you will receive your **API key**.  

### 2. **Test API Access**  
   - Send a **GET request**.
### 🌐 API Endpoint  
```text
https://kindle-vhs5.onrender.com/api/{api_key}
```
   - A **Success** message will confirm that your API is ready to use.

### 3. **Add Books**  
   - To add books, send a **POST request** with the following JSON format:
---

## 🚀 Basic Usage Guidelines  


```
Sample 
```json
{
    "folderName": "Code for Nepa 11/21",
    "bookNames": [
        "Code for Nepal and DataCamp Donates - Data Fellowship 2023",
        "Decoding Trends of NEPSE stock data",
        "Donate to save lives and help Nepalis fight COVID-19 Pandemic"
    ],
    "urls": [
        "https://codefornepal.org/2024/03/25/code_for_nepal_2023_review.html",
        "https://codefornepal.org/2023/12/27/decoding-trends-of-nepse-stock-data-copy.html",
        "https://codefornepal.org/2023/12/20/comprehensive-analysis-of-superstore-sales-trends-and-performance-analysis.html"
    ]
}
```

# Quick Flask Deployment on Render 🚀

Simple guide to deploy your Flask app on Render cloud platform.

## Steps ⚡

1. **Create Requirements File** 📝
```bash
pip freeze > requirements.txt
```

2. **Add Gunicorn** 🌐
```bash
pip install gunicorn

```

3. **Deploy on Render** ☁️
- Create account on [Render](https://render.com)
- New -> Web Service
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

That's it! Your app is live! 🎉

> Note: Replace `app:app` with `your_file_name:app` if needed.
## Acknowledgements

 - [Powered by instapaper api](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 
# 📬 Contact Information

If you have any suggestions or question feel free to reach out to me using the social media handles below:

### 📧 Email
- You can email me at [sharmadi@warhawks.ulm.edu](mailto:sharmadi@warhawks.ulm.edu)

### 🌐 LinkedIn
- Connect with me on LinkedIn: [iamdipeshh](https://www.linkedin.com/in/iamdipeshh/)
  




