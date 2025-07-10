from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ..services.mongodb import MongoDBService
from ..services.websocket import manager
from pydantic import BaseModel
import re

router = APIRouter()

class ChatMessage(BaseModel):
    user_id: str
    message: str

def analyze_query(message: str) -> Dict[str, Any]:
    """Analyze the query type and context from the message"""
    message = message.lower().strip()
    
    # Basic chat patterns
    basic_chat = {
        'chào buổi sáng': 'Chào buổi sáng! Tôi có thể giúp gì cho bạn?',
        'chào buổi chiều': 'Chào buổi chiều! Tôi có thể giúp gì cho bạn?',
        'chào buổi tối': 'Chào buổi tối! Tôi có thể giúp gì cho bạn?',
        'tạm biệt': 'Tạm biệt! Hẹn gặp lại bạn.',
        'cảm ơn': 'Không có gì! Tôi luôn sẵn sàng giúp đỡ bạn.'
    }
    
    for key, response in basic_chat.items():
        if key in message:
            return {
                'type': 'chat',
                'message': response
            }

    # Greeting patterns
    greetings = ['hi', 'hello', 'chào', 'xin chào', 'hey']
    if any(greeting in message for greeting in greetings):
        return {
            'type': 'greeting',
            'message': 'Xin chào! Tôi là trợ lý AI, tôi có thể giúp bạn:\n' + 
                      '• Phân tích sản phẩm bán chạy\n' +
                      '• Theo dõi doanh thu\n' +
                      '• Phân tích khách hàng\n' +
                      '• Dự báo xu hướng bán hàng\n\n' +
                      'Bạn muốn biết thông tin gì?'
        }

    # Small talk patterns
    small_talk = {
        'khỏe không': 'Cảm ơn bạn đã hỏi thăm! Tôi là AI nên luôn trong trạng thái tốt để phục vụ bạn. Bạn cần giúp gì không?',
        'tên gì': 'Tôi là trợ lý AI được tạo ra để giúp bạn phân tích dữ liệu bán hàng. Bạn cần phân tích gì không?',
        'làm được gì': 'Tôi có thể giúp bạn:\n• Phân tích sản phẩm bán chạy\n• Theo dõi doanh thu\n• Phân tích khách hàng\n• Dự báo xu hướng',
        'giúp': 'Tôi có thể giúp bạn phân tích dữ liệu bán hàng. Bạn cần biết thông tin gì?'
    }
    
    for key, response in small_talk.items():
        if key in message:
            return {
                'type': 'chat',
                'message': response
            }

    # Product analysis with enhanced Vietnamese patterns
    product_patterns = [
        r'(sản phẩm|hàng hóa|mặt hàng).*(phổ biến|bán chạy|xuất hiện nhiều|mua nhiều)',
        r'(phổ biến|bán chạy|xuất hiện nhiều|mua nhiều).*(sản phẩm|hàng hóa|mặt hàng)',
        r'(cái gì|gì|món nào).*(bán chạy|mua nhiều)',
        r'top.*(sản phẩm|hàng hóa)',
        r'(sản phẩm|hàng hóa).*(nào|gì).*(nhiều|tốt)',
    ]
    
    if any(re.search(pattern, message) for pattern in product_patterns):
        period = 'all_time'
        if 'tháng này' in message or 'this month' in message:
            period = 'this_month'
        elif 'tháng trước' in message or 'last month' in message:
            period = 'last_month'
            
        trend = None
        if any(word in message for word in ['xu hướng', 'trend', 'biến động', 'thay đổi']):
            trend = 'trend'
            
        context = 'quantity'
        if any(word in message for word in ['doanh thu', 'tiền', 'revenue']):
            context = 'revenue'
            
        return {
            'type': 'top_products',
            'period': period,
            'trend': trend,
            'context': context,
            'intro': 'Dựa trên phân tích dữ liệu bán hàng,'
        }
    
    # Revenue analysis with enhanced patterns
    revenue_patterns = [
        r'(doanh thu|doanh số|bán được|thu nhập|lợi nhuận)',
        r'(bán|thu về).*(nhiều|bao nhiêu).*(tiền)',
        r'(tiền|thu nhập).*(bao nhiêu|như thế nào)',
        r'theo dõi.*(doanh thu|doanh số)',
        r'phân tích.*(doanh thu|doanh số)',
        r'(thống kê|báo cáo).*(doanh thu|doanh số)'
    ]
    
    if any(re.search(pattern, message) for pattern in revenue_patterns):
        period = 'all_time'
        trend = None
        
        if any(word in message for word in ['xu hướng', 'trend', 'biến động', 'thay đổi']):
            trend = 'trend'
        if 'tháng này' in message:
            period = 'this_month'
        elif 'tháng trước' in message:
            period = 'last_month'
            
        return {
            'type': 'revenue_analysis',
            'period': period,
            'trend': trend,
            'intro': 'Theo số liệu thống kê từ hệ thống,'
        }

    # Customer analysis patterns
    customer_patterns = [
        r'(khách hàng|người mua).*(thông tin|phân tích)',
        r'(phân tích|thống kê).*(khách hàng)',
        r'(khách hàng|người mua).*(nào|nhiều)',
        r'(top|những).*(khách hàng)',
        r'thông tin.*(khách hàng)'
    ]
    
    if any(re.search(pattern, message) for pattern in customer_patterns):
        return {
            'type': 'customer_analysis',
            'period': 'all_time',
            'intro': 'Dựa trên dữ liệu khách hàng,'
        }

    # Forecasting patterns
    forecast_patterns = [
        r'(dự báo|dự đoán|phân tích).*(xu hướng|trend)',
        r'(xu hướng|trend).*(bán hàng|doanh thu)',
        r'(dự báo|dự đoán).*(doanh thu|bán hàng)',
        r'(xu hướng|trend).*(tương lai|sắp tới)'
    ]

    if any(re.search(pattern, message) for pattern in forecast_patterns):
        return {
            'type': 'forecast',
            'period': 'future',
            'intro': 'Dựa trên phân tích xu hướng,'
        }

    # Handle unknown queries more naturally
    return {
        'type': 'chat',
        'message': 'Tôi hiểu bạn đang muốn trao đổi, nhưng tôi chưa chắc chắn về ý của bạn. Bạn có thể nói rõ hơn không? Tôi có thể giúp bạn:\n\n' +
                  '• Xem sản phẩm bán chạy nhất\n' +
                  '• Phân tích doanh thu\n' +
                  '• Xem thông tin khách hàng\n' +
                  '• Dự báo xu hướng bán hàng'
    }

@router.post("/chat/message")
async def process_message(
    chat_message: ChatMessage,
    mongodb: MongoDBService = Depends(MongoDBService)
):
    """Process chat messages and return AI response"""
    try:
        query = chat_message.message.strip()
        user_id = chat_message.user_id
        
        if not query:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Tin nhắn không được để trống"}
            )

        # Analyze query intent
        analysis = analyze_query(query)
        response = ""
        
        # Process based on intent type
        if analysis['type'] == 'top_products':
            results = await mongodb.get_top_products(limit=5)
            if not results:
                response = "Xin lỗi, hiện tại chưa có dữ liệu về sản phẩm."
            else:
                response = "Dựa trên dữ liệu bán hàng, đây là top 5 sản phẩm bán chạy nhất:\n\n"
                total_sold = sum(r['total_quantity'] for r in results)
                for i, product in enumerate(results, 1):
                    name = product.get('product_name') or product.get('_id')
                    quantity = product['total_quantity']
                    revenue = product['total_sales']
                    percentage = (quantity / total_sold) * 100 if total_sold else 0
                    response += f"{i}. {name}\n"
                    response += f"   • Số lượng đã bán: {quantity:,} sản phẩm ({percentage:.1f}%)\n"
                    response += f"   • Doanh thu: {revenue:,.0f}đ\n\n"
                response += "\nBạn có muốn biết thêm thông tin chi tiết về sản phẩm nào không?"

        elif analysis['type'] == 'greeting':
            response = analysis['message']

        elif analysis['type'] == 'revenue_analysis':
            results = await mongodb.aggregate_orders([
                {
                    '$group': {
                        '_id': None,
                        'total_revenue': {'$sum': '$sales_per_order'},
                        'total_orders': {'$sum': 1},
                        'total_products': {'$sum': '$order_quantity'}
                    }
                }
            ])
            if not results:
                response = "Xin lỗi, hiện chưa có dữ liệu doanh thu."
            else:
                data = results[0]
                response = f"{analysis['intro']}\n\n"
                response += f"📊 Tổng doanh thu: {data['total_revenue']:,.0f}đ\n"
                response += f"🛍️ Tổng đơn hàng: {data['total_orders']:,}\n"
                response += f"📦 Tổng sản phẩm bán ra: {data['total_products']:,}\n\n"
                response += "Bạn có muốn xem thêm chi tiết về xu hướng doanh thu không?"

        elif analysis['type'] == 'customer_analysis':
            results = await mongodb.get_top_customers(limit=5)
            if not results:
                response = "Xin lỗi, hiện chưa có dữ liệu khách hàng."
            else:
                response = f"{analysis['intro']}\n\n"
                response += "🏆 Top 5 khách hàng có giá trị mua hàng cao nhất:\n\n"
                for i, customer in enumerate(results, 1):
                    response += f"{i}. {customer['customer_name']}\n"
                    response += f"   💰 Tổng chi tiêu: {customer['total_spent']:,.0f}đ\n"
                    response += f"   🛍️ Số đơn hàng: {customer['total_orders']}\n"
                    response += f"   📍 Khu vực: {customer['city']}, {customer['state']}\n\n"
                response += "Bạn có muốn xem thêm thông tin phân tích khách hàng không?"

        elif analysis['type'] == 'forecast':
            results = await mongodb.aggregate_orders([
                {
                    '$group': {
                        '_id': {'$substr': ['$order_date', 6, 4]},  # Năm
                        'year_revenue': {'$sum': '$sales_per_order'}
                    }
                },
                {'$sort': {'_id': 1}}
            ])
            if not results:
                response = "Xin lỗi, chưa đủ dữ liệu để dự báo xu hướng."
            else:
                trend = "tăng" if results[-1]['year_revenue'] > results[0]['year_revenue'] else "giảm"
                response = f"{analysis['intro']}\n\n"
                response += f"📈 Xu hướng doanh thu đang {trend}\n"
                response += "🔍 Dựa trên phân tích các năm gần nhất:\n\n"
                for r in results:
                    response += f"• Năm {r['_id']}: {r['year_revenue']:,.0f}đ\n"
                response += "\nBạn có muốn xem chi tiết dự báo theo từng sản phẩm không?"

        elif analysis['type'] == 'chat':
            response = analysis.get('message', 'Xin lỗi, tôi chưa hiểu rõ câu hỏi của bạn. Vui lòng thử lại.')
        else:
            response = "Xin lỗi, tôi chưa hiểu rõ câu hỏi của bạn. Bạn có thể hỏi về:\n" + \
                      "• Sản phẩm bán chạy nhất\n" + \
                      "• Doanh thu theo thời gian\n" + \
                      "• Thông tin khách hàng\n" + \
                      "\nHoặc gõ 'hướng dẫn' để xem chi tiết hơn."

        # Save conversation
        await mongodb.save_conversation(
            user_id=user_id,
            message=query,
            response=response
        )

        return {
            "status": "success",
            "response": response
        }

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Đã có lỗi xảy ra, vui lòng thử lại sau."
            }
        )
