import io
import uuid
import base64
import qrcode
from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_qr_base64(data_string):
    """Generates a QR code and returns as base64 data URI."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )
    qr.add_data(data_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e1035", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{b64}"

def generate_ticket_pdf(booking):
    """Generates a PDF e-ticket using ReportLab and returns bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    brand_style = ParagraphStyle(
        'BrandTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#7C3AED'),
        spaceAfter=4
    )

    title_style = ParagraphStyle(
        'EventTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#111827'),
        spaceAfter=8
    )

    sub_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=4
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#1F2937')
    )

    story = []

    # Header with EventHub logo and booking reference
    header_data = [
        [
            Paragraph("<b>EventHub</b> <font size=12 color='#6D28D9'>• Official E-Ticket</font>", brand_style),
            Paragraph(f"<font color='#4B5563'>Booking Ref:</font><br/><b>{booking.reference}</b>", bold_label)
        ]
    ]
    header_table = Table(header_data, colWidths=[4.0 * inch, 3.0 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#7C3AED'), spaceAfter=14))

    # Event details banner
    story.append(Paragraph(booking.event.title, title_style))
    story.append(Paragraph(f"<b>Date & Time:</b> {booking.event.start_datetime.strftime('%B %d, %Y at %I:%M %p')}", sub_style))
    story.append(Paragraph(f"<b>Venue:</b> {booking.event.venue}, {booking.event.city}", sub_style))
    story.append(Paragraph(f"<b>Category:</b> {booking.event.category.name if booking.event.category else 'General'}", sub_style))
    story.append(Spacer(1, 14))

    # Attendee info & Booking Details Table
    attendee_info = [
        [Paragraph("<b>Attendee Name:</b>", bold_label), Paragraph(booking.attendee_name, sub_style),
         Paragraph("<b>Status:</b>", bold_label), Paragraph(f"<font color='#059669'><b>{booking.status}</b></font>", bold_label)],
        [Paragraph("<b>Email:</b>", bold_label), Paragraph(booking.attendee_email, sub_style),
         Paragraph("<b>Total Amount:</b>", bold_label), Paragraph(f"<b>₹ {booking.total_amount:,.2f}</b>", bold_label)],
        [Paragraph("<b>Phone:</b>", bold_label), Paragraph(booking.attendee_phone or "N/A", sub_style),
         Paragraph("<b>Payment Status:</b>", bold_label), Paragraph("Paid (Confirmed)", sub_style)]
    ]
    info_table = Table(attendee_info, colWidths=[1.5 * inch, 2.2 * inch, 1.5 * inch, 1.8 * inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 16))

    # Issued Tickets with QR codes
    story.append(Paragraph("<b>Issued Tickets & Entry Barcodes:</b>", bold_label))
    story.append(Spacer(1, 8))

    ticket_rows = [["#", "Ticket Code", "Type", "Status", "Entry QR Code"]]
    tickets = booking.tickets.all()
    for idx, tkt in enumerate(tickets, start=1):
        # Generate QR image flowable
        qr_obj = qrcode.make(tkt.code)
        qr_buf = io.BytesIO()
        qr_obj.save(qr_buf, format="PNG")
        qr_buf.seek(0)
        qr_img = RLImage(qr_buf, width=1.0 * inch, height=1.0 * inch)

        ticket_rows.append([
            str(idx),
            Paragraph(f"<b>{tkt.code}</b>", sub_style),
            Paragraph(tkt.booking_item.ticket_type.name, sub_style),
            Paragraph("Used" if tkt.is_used else "Valid / Unused", sub_style),
            qr_img
        ])

    ticket_table = Table(ticket_rows, colWidths=[0.5 * inch, 2.3 * inch, 1.7 * inch, 1.3 * inch, 1.2 * inch])
    ticket_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7C3AED')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
    ]))
    story.append(ticket_table)
    story.append(Spacer(1, 20))

    # Instructions
    instructions = (
        "<b>Important Instructions:</b><br/>"
        "• Please present this e-ticket (digital or printed) along with a valid government photo ID at the venue entrance.<br/>"
        "• Each ticket QR code is unique and valid for one-time admission only.<br/>"
        "• Rights of admission reserved by the event organizer. Cancellation is subject to platform and organizer refund policy."
    )
    story.append(Paragraph(instructions, sub_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
