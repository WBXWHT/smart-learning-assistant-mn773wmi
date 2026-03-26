import json
import time
import random
from datetime import datetime

# 模拟大模型API调用
class MockLLMClient:
    """模拟大模型客户端，用于语音转写和要点总结"""
    
    def transcribe_audio(self, audio_file_path):
        """
        模拟语音转写功能
        Args:
            audio_file_path: 音频文件路径
        Returns:
            str: 转写后的文本
        """
        print(f"正在转写音频文件: {audio_file_path}")
        time.sleep(1)  # 模拟处理时间
        
        # 模拟转写结果 - 实际项目中这里会调用真正的API
        transcriptions = [
            "今天讲机器学习三大要素：数据、算法、算力。数据要高质量，算法要合适，算力要充足。",
            "深度学习中的卷积神经网络主要用于图像处理，包含卷积层、池化层和全连接层。",
            "Python的列表推导式语法简洁，例如[x*2 for x in range(10)]生成0到18的偶数。"
        ]
        
        return random.choice(transcriptions)
    
    def summarize_text(self, text, max_length=100):
        """
        模拟文本摘要功能
        Args:
            text: 输入文本
            max_length: 摘要最大长度
        Returns:
            dict: 包含摘要和关键点的字典
        """
        print("正在生成要点总结...")
        time.sleep(0.5)
        
        # 模拟摘要生成 - 实际项目中会调用大模型API
        summaries = {
            "机器学习基础": "核心三要素：数据质量决定上限，算法选择影响效果，算力支撑训练过程。",
            "深度学习CNN": "卷积神经网络专为图像设计，通过卷积提取特征，池化降低维度，全连接进行分类。",
            "Python编程技巧": "列表推导式能简化代码，提高可读性，但复杂逻辑建议使用普通循环。"
        }
        
        # 根据输入文本选择最相关的摘要
        if "机器学习" in text:
            summary = summaries["机器学习基础"]
        elif "卷积" in text or "神经网络" in text:
            summary = summaries["深度学习CNN"]
        else:
            summary = summaries["Python编程技巧"]
        
        # 提取关键点
        key_points = []
        sentences = text.split('。')
        for sentence in sentences:
            if sentence and len(sentence) > 10:
                key_points.append(sentence.strip())
                if len(key_points) >= 3:
                    break
        
        return {
            "summary": summary,
            "key_points": key_points,
            "length": len(summary)
        }
    
    def mark_important(self, text, keywords):
        """
        标记重点内容功能
        Args:
            text: 原始文本
            keywords: 要标记的关键词列表
        Returns:
            str: 标记后的文本
        """
        marked_text = text
        for keyword in keywords:
            if keyword in marked_text:
                marked_text = marked_text.replace(keyword, f"【{keyword}】")
        return marked_text

# 学习笔记管理类
class LearningNote:
    """学习笔记类，管理笔记的创建、保存和查看"""
    
    def __init__(self):
        self.notes = []
        self.llm_client = MockLLMClient()
    
    def create_note_from_audio(self, audio_file_path):
        """
        从音频创建学习笔记
        Args:
            audio_file_path: 音频文件路径
        Returns:
            dict: 创建的笔记对象
        """
        print(f"\n{'='*50}")
        print("开始创建学习笔记...")
        
        # 步骤1: 语音转写
        transcript = self.llm_client.transcribe_audio(audio_file_path)
        print(f"转写完成，文本长度: {len(transcript)}字符")
        
        # 步骤2: 要点总结
        summary_result = self.llm_client.summarize_text(transcript)
        
        # 步骤3: 标记重点（迭代功能）
        keywords = ["数据", "算法", "卷积", "神经网络", "Python"]
        marked_transcript = self.llm_client.mark_important(transcript, keywords)
        
        # 创建笔记对象
        note = {
            "id": len(self.notes) + 1,
            "title": f"学习笔记_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "audio_file": audio_file_path,
            "transcript": transcript,
            "marked_transcript": marked_transcript,
            "summary": summary_result["summary"],
            "key_points": summary_result["key_points"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": len(transcript)
        }
        
        self.notes.append(note)
        print(f"笔记创建成功! ID: {note['id']}, 标题: {note['title']}")
        
        return note
    
    def display_note(self, note_id):
        """
        显示笔记详情
        Args:
            note_id: 笔记ID
        """
        note = next((n for n in self.notes if n["id"] == note_id), None)
        
        if not note:
            print(f"未找到ID为{note_id}的笔记")
            return
        
        print(f"\n{'='*50}")
        print(f"笔记ID: {note['id']}")
        print(f"标题: {note['title']}")
        print(f"创建时间: {note['created_at']}")
        print(f"音频文件: {note['audio_file']}")
        print(f"字数统计: {note['word_count']}字")
        print(f"\n【要点总结】")
        print(f"{note['summary']}")
        print(f"\n【关键点】")
        for i, point in enumerate(note['key_points'], 1):
            print(f"{i}. {point}")
        print(f"\n【转写文本（重点已标记）】")
        print(note['marked_transcript'])
        print('='*50)
    
    def list_notes(self):
        """列出所有笔记"""
        print(f"\n{'='*50}")
        print("学习笔记列表:")
        print('-'*50)
        
        if not self.notes:
            print("暂无笔记")
            return
        
        for note in self.notes:
            print(f"ID: {note['id']} | 标题: {note['title']} | "
                  f"创建时间: {note['created_at']} | 字数: {note['word_count']}")
        
        print('='*50)

# 主函数
def main():
    """
    智能学习助手主程序
    模拟语音转写、要点总结和重点标记功能
    """
    print("="*60)
    print("智能学习助手 v1.0")
    print("功能: 语音转写 + 要点总结 + 重点标记")
    print("="*60)
    
    # 初始化学习笔记管理器
    assistant = LearningNote()
    
    # 模拟处理3个音频文件
    audio_files = [
        "lecture_ml_basics.mp3",
        "lecture_deep_learning.mp3", 
        "lecture_python_tips.mp3"
    ]
    
    # 批量创建笔记
    for audio_file in audio_files:
        note = assistant.create_note_from_audio(audio_file)
    
    # 显示所有笔记列表
    assistant.list_notes()
    
    # 显示第一个笔记的详情
    print("\n查看第一个笔记的详细信息:")
    assistant.display_note(1)
    
    # 显示统计信息
    print(f"\n{'='*50}")
    print("使用统计:")
    print(f"总笔记数: {len(assistant.notes)}")
    total_words = sum(note['word_count'] for note in assistant.notes)
    print(f"总字数: {total_words}")
    print("周使用率提升: 35% (模拟数据)")
    print("用户满意度: 4.6/5 (模拟数据)")
    print('='*50)
    print("\n智能学习助手演示完成!")

if __name__ == "__main__":
    main()