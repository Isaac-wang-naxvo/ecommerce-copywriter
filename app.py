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
        "📧 Newsletter 內容重組器",
        "🍴 餐廳菜單文案優化器",
        "🏥 診所衛教文件草稿機",
        "🎥 YouTube 影片腳本大綱器"
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
                    "content": "你是一位專業的內容創作與行銷文案撰寫專家。"
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


# 功能4：Newsletter 內容重組器
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


# =====================
# 功能 5: 餐廳菜單文案優化器
# =====================
elif feature == "🍴 餐廳菜單文案優化器":
    st.header("🍴 餐廳菜單文案優化器")
    st.markdown("將普通菜名升級為美食行銷文案，提升顧客食慾")

    col1, col2 = st.columns(2)
    
    with col1:
        dish_name = st.text_input(
            "原始菜名",
            placeholder="例：炒飯"
        )
        cooking_method = st.text_input(
            "烹飪方式",
            placeholder="例：鑊氣炒、快火焰炒"
        )
    
    with col2:
        core_ingredients = st.text_input(
            "核心食材",
            placeholder="例：松露、松阪豬、北菇"
        )
        special_selling_point = st.text_area(
            "特殊賣點",
            height=80,
            placeholder="例：使用 20 年老滷水、限量供應、招牌秘製"
        )

    if st.button("🚀 優化菜單文案", use_container_width=True, type="primary", key="menu_gen"):
        if not dish_name.strip():
            st.warning("⚠️ 請填寫原始菜名")
        else:
            with st.spinner("正在優化菜單文案..."):
                prompt = f"""
你是一位美食行銷專家。請根據以下菜品資訊，產出升級版的菜單文案。

【原始菜名】：{dish_name}
【烹飪方式】：{cooking_method if cooking_method else "標準烹飪"}
【核心食材】：{core_ingredients if core_ingredients else "基本食材"}
【特殊賣點】：{special_selling_point if special_selling_point else "無特殊說明"}

請提供以下內容（使用 Markdown 格式）：

1. **升級版菜名**（產出 3 個富有創意、誘人的菜名）
2. **菜品描述**（80 字以內，運用感官詞彙如：酥脆、濃郁、香氣撲鼻、入口即化等）
3. **推薦搭配**（建議的飲品或其他菜品搭配，最多 3 個）
4. **用餐建議**（享用方式、最佳溫度或時機等）

請確保文案充滿美食吸引力，能夠激發顧客的食慾。
"""
                result = call_openai_api(prompt, max_tokens=1500)
                
                if result:
                    st.success("✅ 菜單文案優化完成！")
                    st.markdown(result)
                    st.code(result)


# =====================
# 功能 6: 診所衛教文件草稿機
# =====================
elif feature == "🏥 診所衛教文件草稿機":
    st.header("🏥 診所衛教文件草稿機")
    st.markdown("將醫學術語轉化為大眾易懂的衛教文案")

    col1, col2 = st.columns(2)
    
    with col1:
        medical_term = st.text_input(
            "醫學名詞/病症",
            placeholder="例：高血壓、糖尿病、呼吸道感染"
        )
    
    with col2:
        target_audience_health = st.selectbox(
            "目標對象",
            ["一般大眾", "長輩", "家長", "青少年", "患者家屬"]
        )

    if st.button("🚀 產生衛教文件", use_container_width=True, type="primary", key="health_gen"):
        if not medical_term.strip():
            st.warning("⚠️ 請填寫醫學名詞或病症")
        else:
            with st.spinner("正在產生衛教文件..."):
                prompt = f"""
你是一位醫學傳播專家。請根據以下資訊，產出通俗易懂的衛教文件。

【醫學名詞/病症】：{medical_term}
【目標對象】：{target_audience_health}

要求：
1. 將艱澀的醫學術語轉化為大眾易懂的白話文
2. 使用簡單、親切的語言
3. 避免過度醫學化

請提供以下內容（使用 Markdown 格式）：

1. **病症簡介**（用 2-3 句白話文解釋這個病症是什麼）
2. **常見症狀**（列舉 3-4 個常見症狀）
3. **預防重點**（列出 3 個最重要的預防或照護重點，附簡要說明）
4. **日常保健小貼士**（3-4 個實用的日常保健建議）
5. **何時應就醫**（列舉應該立即就醫的警示信號）

請確保內容對 {target_audience_health} 來說清晰易懂。
"""
                result = call_openai_api(prompt, max_tokens=1800)
                
                if result:
                    st.success("✅ 衛教文件產生完成！")
                    
                    # 添加免責聲明
                    full_output = f"""
⚠️ **重要免責聲明**
本內容由 AI 生成，僅供參考之用。如有健康疑慮，請務必諮詢專業醫師進行診斷與治療。

---

{result}

---

⚠️ **重要免責聲明**
本內容由 AI 生成，僅供參考之用。如有健康疑慮，請務必諮詢專業醫師進行診斷與治療。
"""
                    
                    st.markdown(full_output)
                    st.code(full_output)


# =====================
# 功能 7: YouTube 影片腳本大綱器
# =====================
elif feature == "🎥 YouTube 影片腳本大綱器":
    st.header("🎥 YouTube 影片腳本大綱器")
    st.markdown("產出結構化的 YouTube 影片腳本大綱，助您高效規劃影片內容")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        video_topic = st.text_input(
            "影片主題",
            placeholder="例：如何在家做咖啡"
        )
    
    with col2:
        video_audience = st.text_input(
            "目標受眾",
            placeholder="例：咖啡愛好者、初學者"
        )
    
    with col3:
        video_length = st.selectbox(
            "影片預計長度",
            ["5-10 分鐘", "10-15 分鐘", "15-20 分鐘", "20-30 分鐘", "30 分鐘以上"]
        )

    if st.button("🚀 生成影片腳本大綱", use_container_width=True, type="primary", key="youtube_gen"):
        if not video_topic.strip() or not video_audience.strip():
            st.warning("⚠️ 請填寫影片主題與目標受眾")
        else:
            with st.spinner("正在生成 YouTube 腳本大綱..."):
                prompt = f"""
你是一位 YouTube 內容策略師。請根據以下資訊，產出結構化的影片腳本大綱。

【影片主題】：{video_topic}
【目標受眾】：{video_audience}
【影片長度】：{video_length}

要求：
1. 大綱應該符合 {video_length} 的時間安排
2. 針對 {video_audience} 的需求和興趣優化內容
3. 包含時間碼估計

請提供以下內容（使用 Markdown 格式）：

## 📍 Hook 鉤子開場（前 15 秒）
- 一個引人入勝的開場句子，立即抓住觀眾注意力
- 簡單說明影片會帶來什麼價值

## 📋 內容重點（主要段落）
請根據影片長度，提供 3-5 個關鍵內容段落，每個段落包含：
- 段落標題
- 時間估計
- 該段的 2-3 個核心教學點

## 🎯 CTA 結尾（最後 20-30 秒）
- 清楚的行動呼籲（訂閱、按讚、留言、查看相關影片等）
- 簡短的結語
- 下一支影片預告（如適用）

## 💡 補充製作建議
- 建議使用的視覺元素或文字卡
- 可能需要的 B-roll 或示範
"""
                result = call_openai_api(prompt, max_tokens=2500)
                
                if result:
                    st.success("✅ YouTube 腳本大綱產生完成！")
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
- 產業級別的內容品質
- 完整的錯誤處理機制
- 實時預覽與複製功能

### 🆕 新增功能 (v1.2)
- **🍴 餐廳菜單文案優化器**
- **🏥 診所衛教文件草稿機**
- **🎥 YouTube 影片腳本大綱器**

**版本**：v1.2 MVP
""")
