import 'package:flutter/material.dart';
import '../models/message_model.dart';
import '../services/chat.dart';

class ChatViewModel with ChangeNotifier {
  final List<Message> _messages = [];
  final TextEditingController messageController = TextEditingController();

  List<Message> get messages => _messages;

  Future<void> sendMessage(String text) async {
    if (text.isEmpty) return;

    final userMessage = Message(
      text: text,
      type: MessageType.user,
      id: DateTime.now().millisecondsSinceEpoch.toString(),
    );
    _messages.add(userMessage);
    notifyListeners();

    String? loadingId;
    try {
      loadingId = _addLoadingMessage();
      final aiResponse = await ApiService.getAIResponse(text);
      
      _removeMessage(loadingId);
      _addAIMessage(aiResponse);
    } catch (e) {
      _removeMessage(loadingId);
      _addAIMessage("Error: ${e.toString()}");
    }
  }

  String _addLoadingMessage() {
    final loadingMessage = Message(
      text: "Thinking...",
      type: MessageType.loading,
      id: "loading_${DateTime.now().millisecondsSinceEpoch}",
    );
    _messages.add(loadingMessage);
    notifyListeners();
    return loadingMessage.id!;
  }

  void _addAIMessage(String text) {
    _messages.add(Message(
      text: text,
      type: MessageType.ai,
      id: "ai_${DateTime.now().millisecondsSinceEpoch}",
    ));
    notifyListeners();
  }

  void _removeMessage(String? id) {
    if (id == null) return;
    _messages.removeWhere((m) => m.id == id);
    notifyListeners();
  }
}