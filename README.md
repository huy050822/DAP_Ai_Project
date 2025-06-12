# DAP_Ai_Project

## AI-Powered E-Commerce Business Forecasting & Insights

[Figma Design Review](https://www.figma.com/proto/FG44yDBCEHTghcRwFu4Wyi/DAP301m?node-id=63-2983&p=f&t=fiadxzHGGoiNCquo-0&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1)<br>
[Website Review]()


## 📝 Project Description
This project implements an AI-powered e-commerce analytics and forecasting system that provides real-time insights and predictions for business metrics. The system combines real-time data processing, machine learning, and interactive visualization to help businesses make data-driven decisions.

## 🚀 Technologies Used
- **Data Generation & Processing**
  - Python Faker
  - Apache Kafka
  - Apache Spark
- **Database**
  - MongoDB
- **Frontend**
  - HTML/CSS
  - JavaScript
  - Figma
- **AI/ML**
  - Python
  - Scikit-learn
  - TensorFlow/PyTorch
## 📁 Folder structure:
```bash
DAP_Ai_Project/
├── frontend/                        # Giao diện web (HTML/CSS/JS)
│   ├── src/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── images/
│   │   │   ├── Overview.png
│   │   │   └── Overview (1).png
│   │   └── js/
│   │       └── script.js
│   ├── index.html
│   └── dark.html

├── backend/                         # FastAPI backend
│   ├── app/
│   │   ├── main.py                  # FastAPI entrypoint
│   │   ├── routers/
│   │   │   ├── orders.py
│   │   │   ├── forecast.py
│   │   │   └── prompts.py           # NEW: Lưu prompt từ AI
│   │   └── services/
│   │       ├── model.py            # Xử lý model AI / Prophet
│   │       ├── mongodb.py          # NEW: Kết nối MongoDB
│   │       └── prompt_store.py     # NEW: Lưu/truy vấn prompt
│   └── requirements.txt

├── node_backend/                   # (Tuỳ chọn) Node.js backend nếu web cần gọi trực tiếp
│   ├── server.js
│   ├── routes/
│   │   └── prompt.js
│   └── models/
│       └── Prompt.js
│   └── package.json

├── ai_models/                      # Các model AI tích hợp
│   ├── prophet_forecast.py
│   ├── lstm_forecast.py
│   └── huggingface_api.py

├── data_pipeline/                  # Kafka Producer + Spark Consumer
│   ├── kafka_producer.py
│   ├── spark_stream.py
│   └── schema.py

├── datasets/                       # Dataset mẫu
│   └── sample_orders.csv

├── notebooks/                      # Jupyter Notebook test model
│   └── forecasting_test.ipynb

├── docker/                         # Docker hóa toàn bộ project
│   ├── Dockerfile.backend
│   ├── Dockerfile.spark
│   ├── Dockerfile.node             # NEW: Cho node_backend
│   └── docker-compose.yml          # Dịch vụ: FastAPI, Node, MongoDB, Kafka, Spark

├── .env                            # Token HuggingFace, Mongo URI, v.v.
├── README.md
```

## 🛠️ Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/yourusername/DAP_Ai_Project.git
cd DAP_Ai_Project
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up MongoDB
```bash
# Install MongoDB
# Configure MongoDB connection
```

4. Start the application
```bash
python main.py
```

## 📋 Project Workflow

1. **Data Generation**
   - Generate mock data using Faker or Dummy APIs

2. **Real-time Data Streaming**
   - Stream real-time data from the system using Apache Kafka

3. **Real-time Data Processing**
   - Process real-time data with Apache Spark
   - Calculate necessary metrics

4. **Data Storage**
   - Store data in MongoDB

5. **Dashboard Implementation**
   - Design and deploy dashboard in Figma
   - Convert to HTML
   - Connect with MongoDB for real-time data display

6. **Real-time Monitoring**
   - Update and monitor real-time data in the dashboard

7. **AI Integration**
   - Data preparation for Machine Learning
   - Model building
   - System integration for product metrics prediction
   - Model updates and retraining based on new data

## 🤝 Contributing
We welcome contributions to this project! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors
- [Quang Huy](https://github.com/huy050822) - Project Lead
- [Duc Anh](https://github.com/SENULT) - Website
- [Thien An](https://github.com/philipannt) - AI Integration

## 📞 Contact
For any questions or suggestions, please reach out to:
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn Profile] 
