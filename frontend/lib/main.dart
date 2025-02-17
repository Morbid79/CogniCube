import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import './view_models/chat_view_model.dart';
import './views/screens/chat/chat_screen.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => ChatViewModel(),
      child: const App(),
    ),
  );
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Chat',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: Colors.grey[50],
        appBarTheme: const AppBarTheme(
          elevation: 1,
          centerTitle: true,
        ),
      ),
      home: const ChatScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}