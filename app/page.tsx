"use client";

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import { 
  Mic, 
  MicOff, 
  Send, 
  ThumbsUp, 
  ThumbsDown, 
  Brain, 
  Moon, 
  Sparkles,
  MessageCircle,
  Clock,
  User,
  Bot
} from 'lucide-react';

interface DreamInterpretation {
  id: string;
  dreamText: string;
  symbols: Array<{
    symbol: string;
    meaning: string;
    confidence: number;
  }>;
  psychologicalInsights: string[];
  emotionalTone: string;
  timestamp: Date;
  feedback?: 'positive' | 'negative';
  userQuestions?: string[];
}

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

export default function Home() {
  const [dreamText, setDreamText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [interpretation, setInterpretation] = useState<DreamInterpretation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [followUpQuestion, setFollowUpQuestion] = useState('');
  const [isListening, setIsListening] = useState(false);
  
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        if (finalTranscript) {
          setDreamText(prev => prev + finalTranscript);
        }
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);

  const toggleRecording = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const analyzeDream = async () => {
    if (!dreamText.trim()) return;

    setIsAnalyzing(true);
    setAnalysisProgress(0);

    // Simulate analysis progress
    const progressInterval = setInterval(() => {
      setAnalysisProgress(prev => {
        if (prev >= 95) {
          clearInterval(progressInterval);
          return 95;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    try {
      // In a real implementation, this would call the FastAPI backend
      await simulateAnalysis();
      
      const mockInterpretation: DreamInterpretation = {
        id: Date.now().toString(),
        dreamText,
        symbols: [
          { symbol: 'Water', meaning: 'Emotions, subconscious, purification', confidence: 0.85 },
          { symbol: 'Flying', meaning: 'Freedom, ambition, spiritual ascension', confidence: 0.92 },
          { symbol: 'Animals', meaning: 'Instincts, natural desires, hidden aspects', confidence: 0.78 }
        ],
        psychologicalInsights: [
          'This dream suggests a journey of emotional transformation and personal growth.',
          'The presence of water indicates deep emotional processing is occurring.',
          'Flying elements suggest a desire for freedom and transcendence of current limitations.'
        ],
        emotionalTone: 'Transformative',
        timestamp: new Date()
      };

      setInterpretation(mockInterpretation);
      setMessages([
        {
          id: Date.now().toString(),
          type: 'bot',
          content: 'I\'ve analyzed your dream and found several interesting symbolic elements. Would you like me to explain any specific symbol in more detail?',
          timestamp: new Date()
        }
      ]);
      
      setAnalysisProgress(100);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      clearInterval(progressInterval);
      setTimeout(() => setIsAnalyzing(false), 500);
    }
  };

  const simulateAnalysis = () => {
    return new Promise(resolve => setTimeout(resolve, 2000));
  };

  const handleFeedback = (type: 'positive' | 'negative') => {
    if (!interpretation) return;
    
    setInterpretation(prev => prev ? { ...prev, feedback: type } : null);
    
    const feedbackMessage: Message = {
      id: Date.now().toString(),
      type: 'bot',
      content: type === 'positive' 
        ? 'Thank you for the positive feedback! Is there anything specific about this interpretation you\'d like to explore further?'
        : 'I appreciate your feedback. Could you tell me what aspects of the interpretation didn\'t resonate with you?',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, feedbackMessage]);
  };

  const sendFollowUp = () => {
    if (!followUpQuestion.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: followUpQuestion,
      timestamp: new Date()
    };

    const botResponse: Message = {
      id: (Date.now() + 1).toString(),
      type: 'bot',
      content: generateContextualResponse(followUpQuestion),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage, botResponse]);
    setFollowUpQuestion('');
  };

  const generateContextualResponse = (question: string): string => {
    // In a real implementation, this would use GPT for contextual responses
    const responses = [
      'That\'s a fascinating question about your dream symbolism. Dreams often reflect our deepest thoughts and emotions.',
      'Based on your dream content, this symbol typically represents personal transformation and growth.',
      'The psychological significance of this element in your dream suggests inner conflict resolution.',
      'Your subconscious is processing important life transitions through this dream imagery.'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 dark:from-purple-950 dark:via-blue-950 dark:to-indigo-950">
      {/* Header */}
      <header className="border-b bg-white/70 backdrop-blur-md dark:bg-gray-900/70">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-full dark:bg-purple-900">
              <Brain className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                AI Dream Interpreter
              </h1>
              <p className="text-sm text-muted-foreground">Unlock the mysteries of your subconscious</p>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          
          {/* Dream Input Section */}
          <div className="space-y-6">
            <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm dark:bg-gray-900/80">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2">
                  <Moon className="w-5 h-5 text-purple-600" />
                  Tell Me About Your Dream
                </CardTitle>
                <p className="text-sm text-muted-foreground">
                  Describe your dream in detail, or use voice dictation
                </p>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Textarea
                    ref={textareaRef}
                    placeholder="I was walking through a forest when suddenly I could fly above the trees. The water below was crystal clear and I could see my reflection changing into different animals..."
                    value={dreamText}
                    onChange={(e) => setDreamText(e.target.value)}
                    className="min-h-[150px] resize-none border-2 focus:border-purple-500 transition-colors"
                  />
                  <Button
                    variant="outline"
                    size="icon"
                    className={`absolute bottom-3 right-3 transition-all duration-200 ${
                      isListening ? 'bg-red-500 text-white animate-pulse' : 'hover:bg-purple-50'
                    }`}
                    onClick={toggleRecording}
                  >
                    {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                  </Button>
                </div>
                
                {isAnalyzing && (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Sparkles className="w-4 h-4 animate-spin" />
                      Analyzing your dream...
                    </div>
                    <Progress value={analysisProgress} className="h-2" />
                  </div>
                )}

                <Button 
                  onClick={analyzeDream}
                  disabled={!dreamText.trim() || isAnalyzing}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
                  size="lg"
                >
                  {isAnalyzing ? (
                    <>
                      <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                      Interpreting...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Interpret My Dream
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {interpretation && (
              <>
                {/* Symbolic Analysis */}
                <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm dark:bg-gray-900/80">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-blue-600" />
                      Symbolic Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid gap-3">
                      {interpretation.symbols.map((symbol, index) => (
                        <div key={index} className="p-4 rounded-lg border bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-950 dark:to-blue-950">
                          <div className="flex items-center justify-between mb-2">
                            <Badge variant="secondary" className="font-semibold">
                              {symbol.symbol}
                            </Badge>
                            <Badge variant="outline">
                              {Math.round(symbol.confidence * 100)}% confidence
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{symbol.meaning}</p>
                        </div>
                      ))}
                    </div>

                    <Separator />

                    <div>
                      <h4 className="font-semibold mb-2 flex items-center gap-2">
                        <Brain className="w-4 h-4" />
                        Psychological Insights
                      </h4>
                      <div className="space-y-2">
                        {interpretation.psychologicalInsights.map((insight, index) => (
                          <p key={index} className="text-sm text-muted-foreground leading-relaxed">
                            • {insight}
                          </p>
                        ))}
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-4">
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Clock className="w-4 h-4" />
                        Emotional Tone: <Badge variant="outline">{interpretation.emotionalTone}</Badge>
                      </div>
                      
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleFeedback('positive')}
                          className={`transition-colors ${
                            interpretation.feedback === 'positive' 
                              ? 'bg-green-100 text-green-700 border-green-300' 
                              : 'hover:bg-green-50'
                          }`}
                        >
                          <ThumbsUp className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleFeedback('negative')}
                          className={`transition-colors ${
                            interpretation.feedback === 'negative' 
                              ? 'bg-red-100 text-red-700 border-red-300' 
                              : 'hover:bg-red-50'
                          }`}
                        >
                          <ThumbsDown className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Chat Interface */}
                <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm dark:bg-gray-900/80">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <MessageCircle className="w-5 h-5 text-green-600" />
                      Ask Follow-up Questions
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <ScrollArea className="h-[200px] w-full pr-4">
                      <div className="space-y-3">
                        {messages.map((message) => (
                          <div
                            key={message.id}
                            className={`flex gap-3 ${
                              message.type === 'user' ? 'justify-end' : 'justify-start'
                            }`}
                          >
                            <div
                              className={`max-w-[80%] p-3 rounded-lg ${
                                message.type === 'user'
                                  ? 'bg-purple-600 text-white'
                                  : 'bg-gray-100 dark:bg-gray-800'
                              }`}
                            >
                              <div className="flex items-center gap-2 mb-1">
                                {message.type === 'user' ? (
                                  <User className="w-3 h-3" />
                                ) : (
                                  <Bot className="w-3 h-3" />
                                )}
                                <span className="text-xs opacity-70">
                                  {message.timestamp.toLocaleTimeString([], { 
                                    hour: '2-digit', 
                                    minute: '2-digit' 
                                  })}
                                </span>
                              </div>
                              <p className="text-sm">{message.content}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>

                    <div className="flex gap-2">
                      <Textarea
                        placeholder="Ask about specific symbols, request clarification, or explore deeper meanings..."
                        value={followUpQuestion}
                        onChange={(e) => setFollowUpQuestion(e.target.value)}
                        className="resize-none"
                        rows={2}
                      />
                      <Button
                        onClick={sendFollowUp}
                        disabled={!followUpQuestion.trim()}
                        className="shrink-0"
                      >
                        <Send className="w-4 h-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}

            {!interpretation && (
              <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm dark:bg-gray-900/80">
                <CardContent className="py-12 text-center">
                  <Moon className="w-16 h-16 mx-auto text-purple-300 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">Ready to Explore Your Dreams</h3>
                  <p className="text-muted-foreground">
                    Enter your dream above to receive detailed symbolic and psychological interpretations
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}