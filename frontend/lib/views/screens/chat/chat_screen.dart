import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../view_models/chat_view_model.dart';
import '../../../views/components/message_bubble.dart';

class ChatScreen extends StatelessWidget {
  const ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<ChatViewModel>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Chat'),
        elevation: 1,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: true,
              padding: const EdgeInsets.only(top: 16),
              itemCount: viewModel.messages.length,
              itemBuilder: (context, index) {
                final message = viewModel.messages.reversed.toList()[index];
                return MessageBubble(message: message);
              },
            ),
          ),
          _buildInputArea(context),
        ],
      ),
    );
  }

  Widget _buildInputArea(BuildContext context) {
    final viewModel = context.read<ChatViewModel>();

    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: viewModel.messageController,
                decoration: InputDecoration(
                  hintText: 'Type your message...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24),
                  ),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 20),
                ),
                onSubmitted: (text) {
                _sendMessage(context, text);
                viewModel.messageController.clear(); // 新增清空操作
              },
              ),
            ),
            IconButton(
              icon: const Icon(Icons.send_rounded),
              color: Colors.blue,
              onPressed: () => _sendMessage(context, viewModel.messageController.text),
            ),
          ],
        ),
      ),
    );
  }

  void _sendMessage(BuildContext context, String text) {
    if (text.trim().isEmpty) return;
    context.read<ChatViewModel>().sendMessage(text);
    FocusScope.of(context).unfocus();
  }
}