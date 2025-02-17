enum MessageType { user, ai, loading }

class Message {
  final String text;
  final DateTime time;
  final MessageType type;
  final String? id;

  Message({
    required this.text,
    required this.type,
    this.id,
    DateTime? time,
  }) : time = time ?? DateTime.now();
}