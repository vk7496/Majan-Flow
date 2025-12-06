import streamlit as st
import pandas as pd
import time
from PIL import Image

# ---------------------------------------------------------
# 1. Page Configuration (تكوين الصفحة)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Majan Flow IDP",
    page_icon="🇴🇲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (تنسيق مخصص لدعم اللغة العربية)
st.markdown("""
<style>
    .main {
        direction: rtl; /* Set main content to Right-to-Left */
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Mock AI Functions (وظائف محاكاة الذكاء الاصطناعي)
# ---------------------------------------------------------
def simulate_ai_extraction(image):
    """
    This function simulates the output of the Deep Learning model (OCR/IDE).
    وظيفة محاكاة مخرجات نموذج التعلم العميق.
    """
    with st.spinner('جاري معالجة المستند... Processing Document with AI'):
        time.sleep(2)
        
    # Mock Data based on the Omani Invoice Sample
    return {
        "vendor_name": "MUSCAT MODERN LOGISTICS L.L.C",
        "vendor_trn": "OM123456789",
        "invoice_number": "INV-2024-1001",
        "date": "2024-10-15",
        "subtotal": 250.000,
        "tax_amount": 12.500, # Correct VAT 5% for OMR 250
        "total_amount": 262.500,
        "currency": "OMR",
        "line_items": [
            {"الوصف/Description": "Heavy Equipment Transport / خدمات نقل", "الكمية/Qty": 2, "السعر/Price": 100.000, "المجموع/Total": 200.000},
            {"الوصف/Description": "Logistics Consultation / استشارات", "الكمية/Qty": 1, "السعر/Price": 50.000, "المجموع/Total": 50.000}
        ]
    }

def validate_data(data):
    """
    Oman-specific business validation logic (VAT 5% & Math check).
    منطق التحقق التجاري الخاص بسلطنة عمان (5% ضريبة القيمة المضافة والتحقق الرياضي).
    """
    flags = []
    
    # Rule 1: Oman VAT 5% Check (قانون 1: التحقق من ضريبة القيمة المضافة)
    OMAN_VAT_RATE = 0.05
    calculated_tax = data['subtotal'] * OMAN_VAT_RATE
    if abs(calculated_tax - data['tax_amount']) < 0.005:
        flags.append(("SUCCESS", "✅ VAT 5% Match / ضريبة القيمة المضافة صحيحة"))
    else:
        flags.append(("ERROR", f"❌ VAT Error! Expected: {calculated_tax:.3f}, Actual: {data['tax_amount']} / خطأ ضريبة القيمة المضافة"))
        
    # Rule 2: Total Amount Math Check (قانون 2: التحقق من المجموع الإجمالي)
    if abs((data['subtotal'] + data['tax_amount']) - data['total_amount']) < 0.005:
        flags.append(("SUCCESS", "✅ Total Amount Match / المجموع الإجمالي صحيح"))
    else:
        flags.append(("ERROR", "❌ Math Mismatch / خطأ في العمليات الحسابية"))
        
    # Rule 3: Omani TRN Format Check (قانون 3: تنسيق رقم التسجيل الضريبي العماني)
    if data['vendor_trn'].startswith("OM") and len(data['vendor_trn']) > 5:
        flags.append(("SUCCESS", "✅ Valid TRN Format / رقم التسجيل الضريبي صالح"))
    else:
        flags.append(("WARNING", "⚠️ Suspicious TRN Format / تنسيق رقم التسجيل الضريبي مشكوك فيه"))
        
    return flags

# ---------------------------------------------------------
# 3. User Interface (واجهة المستخدم)
# ---------------------------------------------------------

st.title("🇴🇲 Majan Flow: Intelligent Document Processing")
st.markdown("**(مَجان فلو: معالجة المستندات الذكية لسلطنة عمان)**")
st.markdown("---")

# Sidebar Settings (إعدادات الشريط الجانبي)
with st.sidebar:
    st.header("⚙️ Processing Settings / إعدادات المعالجة")
    st.selectbox("نوع المستند / Document Type", ["Invoice (فاتورة)", "ID Card (بطاقة شخصية)", "CR Paper (سجل تجاري)"])
    st.slider("AI Confidence Threshold / عتبة الثقة للذكاء الاصطناعي", 0, 100, 80)
    st.info("This system is designed to demonstrate automation capabilities in Oman. / تم تصميم هذا النظام لعرض إمكانيات الأتمتة في عمان.")

# File Upload Section (قسم تحميل الملفات)
uploaded_file = st.file_uploader("Upload Invoice (PDF or Image) / تحميل الفاتورة (PDF أو صورة)", type=['png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file is not None:
    # Divide the page into two columns (تقسيم الصفحة إلى عمودين)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Original Document / المستند الأصلي")
        image = Image.open(uploaded_file)
        st.image(image, caption='Scanned Document / المستند الممسوح ضوئيًا', use_container_width=True)

    with col2:
        st.subheader("🤖 Extracted Data / البيانات المستخرجة")
        
        if st.button("Start Processing / تشغيل الذكاء الاصطناعي", type="primary"):
            
            # 1. Execute Simulation (تنفيذ المحاكاة)
            extracted_data = simulate_ai_extraction(image)
            
            # 2. Human-in-the-Loop Form (نموذج المراجعة البشرية)
            with st.form("validation_form"):
                c1, c2 = st.columns(2)
                vendor = c1.text_input("Vendor Name / اسم المورد", extracted_data['vendor_name'])
                trn = c2.text_input("TRN (Tax ID) / رقم ضريبي", extracted_data['vendor_trn'])
                
                c3, c4, c5 = st.columns(3)
                subtotal = c3.number_input("Subtotal (OMR) / المجموع الفرعي", value=extracted_data['subtotal'], format="%.3f")
                tax = c4.number_input("VAT (5%) / ضريبة القيمة المضافة", value=extracted_data['tax_amount'], format="%.3f")
                total = c5.number_input("Grand Total (OMR) / المجموع الإجمالي", value=extracted_data['total_amount'], format="%.3f")
                
                # Line Items (بنود الفاتورة)
                st.markdown("##### Line Items / بنود الفاتورة")
                df_items = pd.DataFrame(extracted_data['line_items'])
                st.dataframe(df_items, hide_index=True)

                submitted = st.form_submit_button("Approve & Send to ERP / اعتماد وإرسال إلى نظام ERP")
            
            # 3. Display Validation Results (عرض نتائج التحقق)
            st.markdown("### 🛡️ Validation Report / تقرير التحقق")
            validation_results = validate_data(extracted_data)
            
            for status, msg in validation_results:
                if status == "SUCCESS":
                    st.success(msg)
                elif status == "ERROR":
                    st.error(msg)
                else:
                    st.warning(msg)
            
            # Metrics (المقاييس الرئيسية)
            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total (OMR) / الإجمالي", f"{extracted_data['total_amount']:.3f}")
            m2.metric("Confidence Score / درجة الثقة", "98%")
            m3.metric("Processing Time / زمن المعالجة", "1.2s")

else:
    st.info("Please upload an invoice image to start. / يرجى تحميل صورة فاتورة للبدء.")
    with st.expander("How to test / دليل الاختبار"):
        st.write("""
        1. Upload a sample invoice image with Arabic/English text.
        2. Click 'Start Processing'.
        3. The system will extract data and check Omani tax regulations (5% VAT).
        """)
