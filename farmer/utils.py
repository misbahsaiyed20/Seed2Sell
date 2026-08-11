from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime


def generate_invoice(order):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(220, height - 50, "INVOICE")

    # Order details
    p.setFont("Helvetica", 11)
    p.drawString(50, height - 100, f"Order ID: {order.id}")
    p.drawString(50, height - 120, f"Customer: {order.customer.username}")
    p.drawString(50, height - 140, f"Date: {order.created_at.strftime('%d-%m-%Y')}")

    # Table header
    y = height - 200
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Product")
    p.drawString(250, y, "Quantity")
    p.drawString(350, y, "Price")

    y -= 20
    p.setFont("Helvetica", 11)

    for item in order.items.all():
        p.drawString(50, y, item.product.name)
        p.drawString(250, y, str(item.quantity))
        p.drawString(350, y, f"₹ {item.price}")
        y -= 20

    # Total
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total Amount: ₹ {order.total_amount}")

    # Footer
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, "Thank you for shopping with Seed2Sell")

    p.showPage()
    p.save()

    return response
