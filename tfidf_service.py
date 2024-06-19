from pythainlp import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nomalizing import normalize
from pagerank_service import find_out_link, cal_node, combine_pagerank


class TfidfService:
    TDIDFVECTORIZER = TfidfVectorizer()
    TDIDFVECTOR = None
    DOCS = {'doc-id': [], 'doc-token': [], 'doc-link': [], 'doc-title': [], 'doc-icon': [], 'doc-body': []}

    # the problem is in my inserting web data in my database
    TRASH_WORD = 'เข้าสู่ระบบ MIS บุคลากรคณะ ICSEC2022 การเข้าศึกษา การรับสมัครและคุณสมบัติผู้สมัคร ปฏิทินการศึกษา ค่าธรรมเนียมการศึกษา หลักสูตร ภาควิชา ภาควิชาวิศวกรรมเครื่องกลและการผลิต ภาควิชาวิศวกรรมไฟฟ้าและคอมพิวเตอร์ ภาควิชาวิศวกรรมโยธาและสิ่งแวดล้อม ภาควิชาวิทยาการคอมพิวเตอร์และสารสนเทศ ภาควิชาวิทยาศาสตร์ทั่วไป การรับสมัครและคุณสมบัติผู้สมัคร ปฏิทินการศึกษา ค่าธรรมเนียมการศึกษา 13 หลักสูตร หลักสูตรสาขาวิชาวิศวกรรมโยธา หลักสูตรสาขาวิชาวิศวกรรมไฟฟ้า หลักสูตรสาขาวิชาวิศวกรรมเครื่องกลและการผลิต หลักสูตรสาขาวิชาวิศวกรรมอุตสาหการ หลักสูตรสาขาวิชาวิศวกรรมคอมพิวเตอร์ หลักสูตรสาขาวิชาวิศวกรรมสิ่งแวดล้อมเพื่อการพัฒนาอย่างยั่งยืน หลักสูตรสาขาวิชาวิทยาการคอมพิวเตอร์ หลักสูตรสาขาวิชาเคมีประยุกต์ หลักสูตรสาขาวิชาวิทยาการข้อมูล หลักสูตรสาขาวิชาเทคโนโลยีพลังงานเพื่อความยั่งยืน หลักสูตรสาขาวิชาการจัดการวิศวกรรมและเทคโนโลยี (วศ.ม.) หลักสูตรสาขาวิชาวิศวกรรมไฟฟ้าและคอมพิวเตอร์ (วศ.ม.) หลักสูตรสาขาวิชาวิศวกรรมไฟฟ้าและคอมพิวเตอร์ (ปร.ด.) ภาควิชาวิศวกรรมเครื่องกลและการผลิต ภาควิชาวิศวกรรมไฟฟ้าและคอมพิวเตอร์ ภาควิชาวิศวกรรมโยธาและสิ่งแวดล้อม ภาควิชาวิทยาการคอมพิวเตอร์และสารสนเทศ ภาควิชาวิทยาศาสตร์ทั่วไป ระดับปริญญาตรี ระดับบัณฑิตศึกษา ภาควิชาวิศวกรรมเครื่องกลและการผลิต ภาควิชาวิศวกรรมไฟฟ้าและคอมพิวเตอร์ ภาควิชาวิศวกรรมโยธาและสิ่งแวดล้อม ภาควิชาวิทยาการคอมพิวเตอร์และสารสนเทศ ภาควิชาวิทยาศาสตร์ทั่วไป บุคลากรสำนักงานเลขานุการคณะ สำหรับบุคลากร สำหรับนิสิต ประกาศคณะ ประชาสัมพันธ์ รับเข้าศึกษา วิจัยและบริการวิชาการ วิเทศสัมพันธ์ เทคโนโลยีดิจิทัล ข่าวจ้างเหมา/ประกวดราคา แสดงความยินดี จดหมายเวียน โครงสร้างการบริหาร คณะกรรมการประจำคณะ ประวัติคณะ วิสัยทัศน์ พันธกิจ ทำเนียบคณบดี แผนยุทธศาสตร์ 2563–2567 ระดับปริญญาตรี หลักสูตรที่เปิดสอน ช่องทางการรับเข้าศึกษา คุณสมบัติของผู้สมัคร ค่าธรรมเนียมการศึกษา สมัครเข้าศึกษาต่อ ทุนการศึกษา หอพัก ลิงก์ที่เกี่ยวข้อง สวพ.มก. วช. สวก. อว. NRIIS (วช.) วารสาร การประชุมวิชาการ นำไปใช้ประโยชน์ กลุ่มวิจัยและนวัตกรรมอิเล็กทรอนิกส์ชีวภาพ SMART (Systematic Manufacturing Alternative Research Team) กลุ่มวิจัยพลังงานและสิ่งแวดล้อม กลุ่มวิจัยสมุนไพร กลุ่มวิจัยนวัตกรรมวัสดุ (Innovation Material Research Group) หน่วยบริการเครื่องมือวิทยาศาสตร์ ศูนย์วิจัยสมุนไพร ศูนย์ทดสอบและวิจัยทางด้านวิศวกรรมโยธา งานวิเคราะห์น้ำ ค่ายวิทยาศาสตร์ ผลิตภัณฑ์กัญชา U2T เมนู ออกจากระบบ เกี่ยวกับคณะ ข้อมูลการรับเข้า ข้อมูลภาควิชา ระบบสารสนเทศ ข่าวสาร/ประกาศ ติดต่อ'

    @staticmethod
    def setup_doc(docs_token):
        TfidfService.TDIDFVECTOR = TfidfService.TDIDFVECTORIZER.fit_transform(docs_token)

    @staticmethod
    def set_doc_list(docs):
        TfidfService.DOCS = docs

    @staticmethod
    def query_result(query):
        return TfidfService.TDIDFVECTORIZER.transform([query])

    @staticmethod
    def search(query, result_quantity, docs):
        clear_words = []
        query_word_seg = word_tokenize(query, keep_whitespace=False)

        for i, q_word in enumerate(query_word_seg):
            clear = normalize(q_word)
            clear_words.append(clear)
        query_str = ' '.join(clear_words)

        query_vector = TfidfService.query_result(query_str)
        similarity_scores = list(enumerate(cosine_similarity(query_vector, TfidfService.TDIDFVECTOR)[0]))
        sorted_similar_docs = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        link_nodes = []
        similarity_tuple = {}
        for i, (tfidf_id, similarity_score) in enumerate(sorted_similar_docs[:result_quantity]):
            link = docs['doc-link'][tfidf_id]
            find_out_link(docs['doc-id'][tfidf_id], docs['doc-link'][:result_quantity], link_nodes)
            similarity_tuple[link] = {
                "tfidf_id": tfidf_id,
                "score": similarity_score,
            }

        popular_links = cal_node(link_nodes)
        return combine_pagerank(docs, popular_links, similarity_tuple, TfidfService.TRASH_WORD)
