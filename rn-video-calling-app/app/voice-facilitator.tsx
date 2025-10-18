import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  SafeAreaView,
  Animated,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, router } from 'expo-router';
import { LiveKitRoom, useRoomContext, useLocalParticipant, useTracks } from '@livekit/react-native';
import { Track } from 'livekit-client';
import { API_BASE_URL } from '../config/api';

interface ConversationData {
  room_name: string;
  user_token: string;
  conversation_starters: string[];
  common_interests: string[];
  livekit_url: string;
}

// Animated Microphone Component
const AnimatedMicrophone = ({ isAgentSpeaking, isMicEnabled }: { isAgentSpeaking: boolean; isMicEnabled: boolean }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (isAgentSpeaking) {
      // Wave animation when agent is speaking
      Animated.loop(
        Animated.sequence([
          Animated.timing(scaleAnim, {
            toValue: 1.2,
            duration: 400,
            useNativeDriver: true,
          }),
          Animated.timing(scaleAnim, {
            toValue: 0.9,
            duration: 400,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      // Reset to normal
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }).start();
    }
  }, [isAgentSpeaking]);

  useEffect(() => {
    // Subtle pulse when mic is enabled
    if (isMicEnabled && !isAgentSpeaking) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.05,
            duration: 1500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1500,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      Animated.timing(pulseAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }).start();
    }
  }, [isMicEnabled, isAgentSpeaking]);

  return (
    <Animated.View
      style={{
        transform: [
          { scale: isAgentSpeaking ? scaleAnim : pulseAnim }
        ],
      }}
      className="items-center justify-center"
    >
      <View className={`w-48 h-48 rounded-full items-center justify-center ${
        isMicEnabled ? 'bg-gradient-to-br from-pink-500 to-purple-600' : 'bg-gray-400'
      }`}
      style={{
        shadowColor: isMicEnabled ? '#ec4899' : '#666',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.3,
        shadowRadius: 20,
        elevation: 10,
      }}>
        <Ionicons 
          name={isMicEnabled ? "mic" : "mic-off"} 
          size={80} 
          color="white" 
        />
      </View>
      
      {/* Outer glow rings when speaking */}
      {isAgentSpeaking && (
        <>
          <View className="absolute w-56 h-56 rounded-full border-4 border-pink-300 opacity-30" />
          <View className="absolute w-64 h-64 rounded-full border-2 border-pink-200 opacity-20" />
        </>
      )}
    </Animated.View>
  );
};

// Audio Visualizer Bars
const AudioVisualizer = ({ isActive }: { isActive: boolean }) => {
  const bars = Array.from({ length: 40 });
  const animations = useRef(bars.map(() => new Animated.Value(0.3))).current;

  useEffect(() => {
    if (isActive) {
      animations.forEach((anim, index) => {
        Animated.loop(
          Animated.sequence([
            Animated.timing(anim, {
              toValue: Math.random() * 0.7 + 0.3,
              duration: 150 + Math.random() * 200,
              useNativeDriver: false,
            }),
            Animated.timing(anim, {
              toValue: 0.3,
              duration: 150 + Math.random() * 200,
              useNativeDriver: false,
            }),
          ]),
          { iterations: -1 }
        ).start();
      });
    } else {
      animations.forEach(anim => {
        Animated.timing(anim, {
          toValue: 0.3,
          duration: 200,
          useNativeDriver: false,
        }).start();
      });
    }
  }, [isActive]);

  return (
    <View className="flex-row items-center justify-center h-16 gap-1">
      {animations.map((anim, index) => (
        <Animated.View
          key={index}
          style={{
            height: anim.interpolate({
              inputRange: [0, 1],
              outputRange: ['20%', '100%'],
            }),
            width: 3,
            backgroundColor: isActive ? '#ec4899' : '#d1d5db',
            borderRadius: 2,
          }}
        />
      ))}
    </View>
  );
};

export default function VoiceFacilitatorScreen() {
  const { otherUser, currentUser } = useLocalSearchParams<{ 
    otherUser: string; 
    currentUser: string; 
  }>();
  
  const [conversationData, setConversationData] = useState<ConversationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMicEnabled, setIsMicEnabled] = useState(true);
  const [isConnected, setIsConnected] = useState(false);
  const [isAgentSpeaking, setIsAgentSpeaking] = useState(false);

  useEffect(() => {
    initializeConversation();
  }, []);

  const initializeConversation = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE_URL}/api/start-facilitated-conversation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user1: currentUser,
          user2: otherUser,
          room_name: `facilitated-${Date.now()}-${Math.random().toString(36).substring(7)}`
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to start conversation');
      }

      const data: ConversationData = await response.json();
      setConversationData(data);
      
      // Launch facilitator agent
      await fetch(`${API_BASE_URL}/api/launch-facilitator`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          room_name: data.room_name,
          user1: currentUser,
          user2: otherUser
        }),
      });

    } catch (error) {
      console.error('Error initializing conversation:', error);
      setError('Failed to start conversation');
    } finally {
      setLoading(false);
    }
  };

  const handleEndCall = () => {
    Alert.alert(
      'End Conversation',
      'Are you sure you want to end this conversation?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'End', 
          style: 'destructive',
          onPress: () => router.back()
        }
      ]
    );
  };

  const handleMicToggle = () => {
    setIsMicEnabled(!isMicEnabled);
  };

  if (loading) {
    return (
      <SafeAreaView className="flex-1 bg-gradient-to-b from-pink-50 to-purple-50 items-center justify-center">
        <View className="items-center">
          <ActivityIndicator size="large" color="#ec4899" />
          <Text className="text-gray-700 mt-6 text-xl font-semibold">Setting up your date...</Text>
          <Text className="text-gray-500 mt-2 text-sm text-center px-8">
            Our AI is analyzing your memories and preparing conversation topics
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView className="flex-1 bg-gradient-to-b from-pink-50 to-purple-50">
        <View className="flex-1 items-center justify-center p-8">
          <View className="bg-white rounded-3xl p-8 items-center shadow-lg">
            <View className="bg-red-100 w-20 h-20 rounded-full items-center justify-center mb-4">
              <Ionicons name="alert-circle" size={50} color="#ef4444" />
            </View>
            <Text className="text-gray-800 text-2xl font-bold text-center mb-2">
              Connection Failed
            </Text>
            <Text className="text-gray-600 text-center mb-6">
              {error}
            </Text>
            <TouchableOpacity
              onPress={() => router.back()}
              className="bg-pink-500 px-8 py-4 rounded-full"
            >
              <Text className="text-white font-semibold text-lg">Go Back</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>
    );
  }

  if (!conversationData) {
    return null;
  }

  return (
    <SafeAreaView className="flex-1 bg-gradient-to-b from-pink-50 via-purple-50 to-pink-50">
      <LiveKitRoom
        serverUrl={conversationData.livekit_url}
        token={conversationData.user_token}
        connect={true}
        audio={true}
        video={false}
        onConnected={() => setIsConnected(true)}
        onDisconnected={() => setIsConnected(false)}
      >
        {/* Minimal Header */}
        <View className="px-6 pt-4 pb-2">
          <View className="flex-row items-center justify-between">
            <TouchableOpacity 
              onPress={handleEndCall}
              className="w-10 h-10 rounded-full bg-white items-center justify-center"
              style={{
                shadowColor: '#000',
                shadowOffset: { width: 0, height: 2 },
                shadowOpacity: 0.1,
                shadowRadius: 4,
                elevation: 3,
              }}
            >
              <Ionicons name="chevron-back" size={24} color="#ec4899" />
            </TouchableOpacity>

            <View className="flex-row items-center">
              <View className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-gray-400'}`} />
              <Text className="text-gray-600 text-sm font-medium">
                {isConnected ? 'Live' : 'Connecting...'}
              </Text>
            </View>
          </View>
        </View>

        {/* Main Content */}
        <View className="flex-1 justify-between py-8">
          {/* Top Section - Audio Visualizer */}
          <View className="px-6">
            <AudioVisualizer isActive={isAgentSpeaking || isConnected} />
          </View>

          {/* Center Section - Big Animated Microphone */}
          <View className="items-center justify-center flex-1">
            <AnimatedMicrophone 
              isAgentSpeaking={isAgentSpeaking} 
              isMicEnabled={isMicEnabled}
            />
            
             <Text className="text-gray-800 text-2xl font-bold mt-8">
               {currentUser} & {otherUser}
             </Text>
            <Text className="text-gray-500 text-sm mt-1">
              {isAgentSpeaking ? 'AI Facilitator speaking...' : 'Listening...'}
            </Text>
          </View>

          {/* Bottom Section - Controls */}
          <View className="px-6">
            <View className="flex-row justify-center items-center gap-6 mb-4">
              {/* Mute Button */}
              <TouchableOpacity
                onPress={handleMicToggle}
                className={`w-16 h-16 rounded-full items-center justify-center ${
                  isMicEnabled ? 'bg-white' : 'bg-red-500'
                }`}
                style={{
                  shadowColor: '#000',
                  shadowOffset: { width: 0, height: 4 },
                  shadowOpacity: 0.1,
                  shadowRadius: 8,
                  elevation: 5,
                }}
              >
                <Ionicons 
                  name={isMicEnabled ? "mic" : "mic-off"} 
                  size={28} 
                  color={isMicEnabled ? "#ec4899" : "white"} 
                />
              </TouchableOpacity>
              
              {/* End Call Button */}
              <TouchableOpacity
                onPress={handleEndCall}
                className="w-20 h-20 rounded-full bg-red-500 items-center justify-center"
                style={{
                  shadowColor: '#ef4444',
                  shadowOffset: { width: 0, height: 4 },
                  shadowOpacity: 0.3,
                  shadowRadius: 8,
                  elevation: 5,
                }}
              >
                <Ionicons name="call" size={32} color="white" />
              </TouchableOpacity>

              {/* Placeholder for symmetry */}
              <View className="w-16 h-16" />
            </View>

            {/* Status Text */}
            <Text className="text-center text-gray-600 text-sm">
              {isMicEnabled ? 'Tap to mute' : 'Tap to unmute'}
            </Text>
          </View>
        </View>
      </LiveKitRoom>
    </SafeAreaView>
  );
}