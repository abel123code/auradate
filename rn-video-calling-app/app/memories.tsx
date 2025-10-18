import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, router } from 'expo-router';
import { API_BASE_URL } from '../config/api';

interface Memory {
  memory: string;
  timestamp?: string;
  metadata?: {
    timestamp?: string;
    role?: string;
  };
}

interface UserMemoriesResponse {
  username: string;
  memories: Memory[];
  count: number;
}

export default function MemoriesScreen() {
  const { username } = useLocalSearchParams<{ username: string }>();
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (username) {
      fetchUserMemories();
    }
  }, [username]);

  const fetchUserMemories = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}/api/user-memories/${encodeURIComponent(username)}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          setError('User not found');
        } else {
          setError('Failed to load memories');
        }
        return;
      }

      const data: UserMemoriesResponse = await response.json();
      setMemories(data.memories || []);
    } catch (error) {
      console.error('Error fetching user memories:', error);
      setError('Failed to load memories');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    router.back();
  };

  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) return '';
    
    try {
      const date = new Date(timestamp);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    } catch {
      return timestamp;
    }
  };

  if (loading) {
    return (
      <View className="flex-1 bg-pink-50 items-center justify-center">
        <ActivityIndicator size="large" color="#ec4899" />
        <Text className="text-gray-600 mt-4">Loading memories...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 bg-pink-50">
        <View className="p-4 bg-white border-b border-pink-200 shadow-sm">
          <TouchableOpacity onPress={handleBack} className="flex-row items-center mb-4">
            <Ionicons name="arrow-back" size={24} color="#ec4899" />
            <Text className="text-gray-800 ml-2 text-lg font-semibold">Back to Search</Text>
          </TouchableOpacity>
        </View>

        <View className="flex-1 items-center justify-center p-8">
          <Ionicons name="alert-circle-outline" size={80} color="#ef4444" />
          <Text className="text-gray-800 text-xl font-semibold mt-4 mb-2">
            {error}
          </Text>
          <Text className="text-gray-600 text-center">
            {error === 'User not found' 
              ? `No user found with username "${username}"`
              : 'Please try again later'
            }
          </Text>
          <TouchableOpacity
            onPress={handleBack}
            className="mt-6 bg-pink-600 px-6 py-3 rounded-lg"
          >
            <Text className="text-white font-semibold">Back to Search</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-pink-50">
      {/* Fixed Header */}
      <View className="p-4 bg-white border-b border-pink-200 shadow-sm">
        <TouchableOpacity onPress={handleBack} className="flex-row items-center mb-4">
          <Ionicons name="arrow-back" size={24} color="#ec4899" />
          <Text className="text-gray-800 ml-2 text-lg font-semibold">Back to Search</Text>
        </TouchableOpacity>
        
        <View className="bg-pink-50 p-4 rounded-lg border border-pink-200">
          <Text className="text-xl font-bold text-gray-800 mb-1">
            {username}
          </Text>
          <Text className="text-gray-600 text-sm">
            {memories.length} {memories.length === 1 ? 'memory' : 'memories'} found
          </Text>
        </View>
      </View>

      {/* Scrollable Content */}
      {memories.length === 0 ? (
        <View className="flex-1 items-center justify-center p-8">
          <Ionicons name="time-outline" size={80} color="#6b7280" />
          <Text className="text-gray-600 text-center mt-4 text-lg">
            No memories found
          </Text>
          <Text className="text-gray-500 text-center mt-2">
            This user hasn't had any conversations yet
          </Text>
        </View>
      ) : (
        <ScrollView 
          className="flex-1" 
          contentContainerStyle={{ padding: 16 }}
          showsVerticalScrollIndicator={true}
        >
          <Text className="text-gray-800 text-lg font-semibold mb-4">
            💭 Memories
          </Text>

          {memories.map((memory, index) => (
            <View
              key={index}
              className="bg-white p-4 rounded-lg mb-3 border border-pink-200 shadow-sm"
            >
              <View className="flex-row items-start">
                <View className="bg-pink-600 w-8 h-8 rounded-full items-center justify-center mr-3 mt-0.5">
                  <Text className="text-white font-bold text-sm">{index + 1}</Text>
                </View>
                <View className="flex-1">
                  <Text className="text-gray-800 text-base leading-6 mb-2">
                    {memory.memory}
                  </Text>
                  {memory.metadata?.timestamp && (
                    <Text className="text-gray-500 text-xs">
                      {formatTimestamp(memory.metadata.timestamp)}
                    </Text>
                  )}
                </View>
              </View>
            </View>
          ))}

          <View className="bg-white p-4 rounded-lg mt-4 border border-pink-200 shadow-sm">
            <Text className="text-gray-600 text-sm">
              💡 These are the memories from {username}'s conversations with AI dating companions.
            </Text>
          </View>
        </ScrollView>
      )}
    </View>
  );
}
