import streamlit as st
from openai import OpenAI, APIError, AuthenticationError
import time

# 設定頁面配置
st.set_page_config(
    page_title="AI 電商行銷助手",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 側邊欄設定
st.sidebar.title("⚙️ 設定")
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

# 功能選擇菜單
st.sidebar.markdown("---")
st.sidebar.title("🎯 功能選擇")
feature = st.sidebar.radio(
    "選擇您要使用的功能",
    options=[
        "📦 電商商品文案生成器",
        "🔄 廣告標題 A/B 測試生成器",
        "❓ SEO FAQ 批量生成器",
        "📧 Newsletter 內容重組器"
    ]
)

# 初始化 OpenAI 客戶端函數
def get_openai_client():
    """取得 OpenAI 客戶端，並驗證 API Key"""
    if not api_key or api_key.strip() == "":
        st.error("❌ 請在左側邊欄輸入 OpenAI API Key")
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        # 驗證 API Key 的有效性
        return client
    except AuthenticationError:
        st.error("❌ API Key 無效，請檢查並重新輸入")
        return None
    except Exception as e:
        st.error(f"❌ 客戶端初始化失敗：{str(e)}")
        return None


def call_openai_api(prompt, max_tokens=2000):
    """呼叫 OpenAI API"""
    client = get_openai_client()
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位專業的電商行銷文案撰寫專家。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except AuthenticationError:
        st.error("❌ API Key 驗證失敗，請檢查 API Key 是否正確")
        return None
    except APIError as e:
        st.error(f"❌ API 呼叫失敗：{str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ 發生未預期的錯誤：{str(e)}")
        return None


# 功能1：電商商品文案生成器
if feature == "📦 電商商品文案生成器":
    st.title("📦 電商商品文案生成器")
    st.markdown("**輸入商品資訊，自動產生 SEO 最佳化的標題與描述**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input(
            "商品名稱",
            placeholder="例：高級咖啡豆"
        )
        product_spec = st.text_area(
            "商品規格",
            placeholder="例：500克包裝、單源豆、中度烘焙、評分8.5/10"
        )
    
    with col2:
        keywords = st.text_input(
            "目標關鍵字（用逗號分隔）",
            placeholder="例：精品咖啡，衣索比亞豆，新鮮烘焙"
        )
    
    if st.button("🚀 生成文案", key="product_gen"):
        if not product_name.strip() or not product_spec.strip():
            st.warning("⚠️ 請填寫商品名稱與規格")
        else:
            with st.spinner("正在生成文案..."):
                prompt = f"""
請根據以下商品資訊生成 SEO 最佳化的電商文案：

【商品名稱】：{product_name}
【商品規格】：{product_spec}
【目標關鍵字】：{keywords if keywords else "無特定關鍵字"}

請提供以下內容（使用 Markdown 格式）：

1. **SEO 標題**（50-60字，包含主要關鍵字）
2. **簡短描述**（100-150字）
3. **詳細描述**（200-300字）
4. **推薦關鍵字**（5-8個）
5. **標籤建議**（5-10個）
"""
                result = call_openai_api(prompt)
                if result:
                    st.success("✅ 文案生成成功！")
                    st.markdown(result)
                    
                    # 複製按鈕
                    st.code(result)


# 功能2：廣告標題 A/B 測試生成器
elif feature == "🔄 廣告標題 A/B 測試生成器":
    st.title("🔄 廣告標題 A/B 測試生成器")
    st.markdown("**輸入受眾與產品資訊，一次產出 10 組不同行銷角度的文案組合**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_audience = st.text_input(
            "目標受眾描述",
            placeholder="例：25-35 歲的上班族，關注健康與效率"
        )
    
    with col2:
        product_desc = st.text_input(
            "產品簡述",
            placeholder="例：一款高效能的時間管理 App"
        )
    
    if st.button("🚀 生成 10 組文案", key="ab_gen"):
        if not target_audience.strip() or not product_desc.strip():
            st.warning("⚠️ 請填寫目標受眾與產品資訊")
        else:
            with st.spinner("正在生成 10 組廣告標題..."):
                prompt = f"""
請根據以下資訊生成 10 組不同行銷角度的廣告標題組合（A/B 測試用）：

【目標受眾】：{target_audience}
【產品介紹】：{product_desc}

要求：
- 每組包含一個主要標題 + 一個副標題
- 涵蓋不同的行銷角度（如：價值訴求、痛點解決、限時優惠、社群認可等）
- 每個標題控制在 30 字以內
- 使用醒目、有吸引力的語言

請按照以下格式輸出：

**第 1 組 - 角度：[行銷角度]**
- A 標題：[主標題]
- B 標題：[副標題或變異版]

（重複 10 次）
"""
                result = call_openai_api(prompt, max_tokens=3000)
                if result:
                    st.success("✅ 廣告標題生成成功！")
                    st.markdown(result)
                    st.code(result)


# 功能3：SEO FAQ 批量生成器
elif feature == "❓ SEO FAQ 批量生成器":
    st.title("❓ SEO FAQ 批量生成器")
    st.markdown("**輸入關鍵字，自動產生 5 組 SEO 最佳化的常見問答**")
    
    keywords_input = st.text_input(
        "輸入目標關鍵字",
        placeholder="例：如何選擇咖啡豆"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        faq_count = st.slider(
            "產生 FAQ 數量",
            min_value=3,
            max_value=10,
            value=5,
            step=1
        )
    
    if st.button("🚀 生成 FAQ", key="faq_gen"):
        if not keywords_input.strip():
            st.warning("⚠️ 請輸入至少一個關鍵字")
        else:
            with st.spinner(f"正在生成 {faq_count} 組 FAQ..."):
                prompt = f"""
請根據以下關鍵字生成 {faq_count} 組 SEO 最佳化的常見問答（FAQ）：

【目標關鍵字】：{keywords_input}

要求：
- 每個問題應包含目標關鍵字或相關變異詞
- 答案應詳細、實用，200 字左右
- 涵蓋常見問題與業務相關的關鍵問題
- 格式清晰易讀
- 考慮用戶搜尋意圖，提高 SEO 排名機率

請按照以下格式輸出：

**Q1：[問題]**
A：[詳細答案]

**Q2：[問題]**
A：[詳細答案]

（重複 {faq_count} 次）

最後請提供一份 SEO 優化建議。
"""
                result = call_openai_api(prompt, max_tokens=3500)
                if result:
                    st.success(f"✅ {faq_count} 組 FAQ 生成成功！")
                    st.markdown(result)
                    st.code(result)


# =====================
# 功能 4: Newsletter 內容重組器
# =====================
elif feature == "📧 Newsletter 內容重組器":
    st.header("📧 Newsletter 內容重組器")
    st.markdown("將長篇文章自動拆解、重組為適合電子報發送的精簡段落")

    source_text = st.text_area(
        "輸入長篇文章內容",
        height=300,
        placeholder="請貼上您想轉換的長篇文章或部落格內容..."
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "電子報語氣",
            ["專業嚴謹", "親切幽默", "激勵人心", "簡約直白"]
        )
    with col2:
        target_reader = st.text_input(
            "目標讀者",
            placeholder="例：創業者、行銷新手"
        )

    if st.button("🚀 重組為電子報內容", use_container_width=True, type="primary", key="newsletter_gen"):
        if not source_text.strip():
            st.warning("⚠️ 請提供來源文章內容")
        elif not target_reader.strip():
            st.warning("⚠️ 請填寫目標讀者")
        else:
            with st.spinner("正在重組電子報內容..."):
                prompt = f"""
請將以下長篇文章改寫為適合 Newsletter（電子報）發送的格式。

【目標語氣】：{tone}
【目標讀者】：{target_reader}
【原文內容】：
{source_text}

要求：
1. **主旨列 (Subject Line)**：產出 3 個高開啟率的標題。
2. **引言 (Hook)**：一段引人入勝的開場，吸引讀者繼續閱讀。
3. **精簡段落**：將原文拆解為 3 個帶有子標題的重點段落，每段不超過 100 字。
4. **行動呼籲 (CTA)**：一個具備導購或點擊驅動力的結尾。

請使用 Markdown 格式輸出。
"""
                result = call_openai_api(prompt, max_tokens=2000)
                
                if result:
                    st.success("✅ 電子報重組完成！")
                    st.markdown(result)
                    st.code(result)


# 頁腳說明
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📖 使用說明
1. 在上方輸入您的 OpenAI API Key
2. 選擇所需功能
3. 填寫相應資訊
4. 點擊按鈕自動生成

### ⚡ 功能特點
- 使用 GPT-4o Mini 模型
- 產業級別的行銷文案品質
- 完整的錯誤處理機制
- 實時預覽與複製功能

### 📧 新增功能
- **Newsletter 內容重組器** v1.0
  將長文轉換為電子報格式

**版本**：v1.1 MVP
""")
