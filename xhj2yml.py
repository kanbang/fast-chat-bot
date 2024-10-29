import yaml

def xhj_to_chatterbot_yml(txt_file_path, yml_file_path, batch_size=1000):
    with open(txt_file_path, 'r', encoding='utf-8') as file, open(yml_file_path, 'w', encoding='utf-8') as yml_file:
        yml_file.write("categories:\n- xhj_dialogues\nconversations:\n")
        
        conversation_batch = []
        conversation_count = 0  # 使用会话计数器
        conversation = []

        for line in file:
            line = line.strip()

            # 检测 'E' 表示新对话的开始
            if line.startswith('E'):
                # 如果已经有积累的对话，保存它
                if len(conversation) == 2:
                    conversation_batch.append(conversation)
                    conversation_count += 1  # 增加会话计数
                else:
                    print(f"对话对不完整: {conversation}")
                    
                conversation = []  # 重置对话

                # 每 batch_size 个会话写入一次文件
                if conversation_count >= batch_size:
                    yaml.safe_dump(conversation_batch, yml_file, allow_unicode=True, default_flow_style=False, explicit_start=False)
                    print(f"写入 {conversation_count} 个会话")
                    conversation_batch = []  # 清空批次缓存
                    conversation_count = 0

            # 收集 'M' 开头的行
            elif line.startswith('M'):
                dialogue_line = line[2:].strip()
                if dialogue_line:  # 确保不是空白行
                    conversation.append(dialogue_line)

        # 写入剩余的对话
        if conversation_batch:
            yaml.safe_dump(conversation_batch, yml_file, allow_unicode=True, default_flow_style=False, explicit_start=False)

        # 写入最后未满 batch_size 的对话
        if len(conversation) == 2:
            yaml.safe_dump([conversation], yml_file, allow_unicode=True, default_flow_style=False, explicit_start=False)


if __name__ == '__main__':
    # 使用优化函数将 xhj.txt 转换为 chatterbot_corpus.yml，每 1000 个会话写一次
    txt_file = './docs/xiaohuangji50w_nofenci.conv'
    yml_file = './custom_corpus/xiaohuangji.yml'
    xhj_to_chatterbot_yml(txt_file, yml_file, batch_size=1000)
