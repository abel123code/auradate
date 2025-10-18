import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { API_BASE_URL } from '../../config/api';

interface User {
  id: string;
  display_name: string;
}

export default function SparkScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<User[]>([]);
  const [searching, setSearching] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      Alert.alert('Error', 'Please enter a username to search');
      return;
    }

    setSearching(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/users`);
      const data = await response.json();
      
      // Filter users by search query (case-insensitive partial match)
      const filteredUsers = data.users.filter((user: User) => 
        user.display_name.toLowerCase().includes(searchQuery.toLowerCase())
      );
      
      setSearchResults(filteredUsers);
    } catch (error) {
      console.error('Error searching users:', error);
      Alert.alert('Error', 'Failed to search users');
    } finally {
      setSearching(false);
    }
  };

  const handleUserSelect = (user: User) => {
    router.push({
      pathname: '/memories',
      params: { username: user.display_name }
    });
  };

  return (
    <View className="flex-1 bg-pink-50">
      <View className="p-4 bg-white border-b border-pink-200 shadow-sm">
        <Text className="text-gray-800 text-lg font-semibold mb-2">
          🔍 Search Users
        </Text>
        <Text className="text-gray-600 text-sm">
          Search for users to view their memories and dating history
        </Text>
      </View>

      <View className="p-4">
        <View className="bg-white p-4 rounded-lg border border-pink-200 shadow-sm mb-4">
          <Text className="text-gray-800 font-semibold mb-2">Username Search</Text>
          <TextInput
            value={searchQuery}
            onChangeText={setSearchQuery}
            placeholder="Enter username to search..."
            className="bg-gray-50 border border-gray-300 rounded-lg px-3 py-3 text-gray-800 mb-3"
            placeholderTextColor="#9CA3AF"
          />
          <TouchableOpacity
            onPress={handleSearch}
            disabled={searching || !searchQuery.trim()}
            className={`rounded-lg px-6 py-3 ${
              searching || !searchQuery.trim() 
                ? 'bg-gray-400' 
                : 'bg-pink-600'
            }`}
          >
            {searching ? (
              <View className="flex-row items-center justify-center">
                <ActivityIndicator size="small" color="white" />
                <Text className="text-white font-semibold ml-2">Searching...</Text>
              </View>
            ) : (
              <Text className="text-white font-semibold text-center">Search</Text>
            )}
          </TouchableOpacity>
        </View>

        {searchResults.length > 0 && (
          <View className="bg-white rounded-lg border border-pink-200 shadow-sm">
            <View className="p-4 border-b border-pink-200">
              <Text className="text-gray-800 font-semibold">
                Search Results ({searchResults.length})
              </Text>
            </View>
            <ScrollView className="max-h-64">
              {searchResults.map((user) => (
                <TouchableOpacity
                  key={user.id}
                  onPress={() => handleUserSelect(user)}
                  className="p-4 border-b border-pink-100 flex-row items-center"
                  activeOpacity={0.7}
                >
                  <View className="bg-pink-600 w-10 h-10 rounded-full items-center justify-center mr-3">
                    <Ionicons name="person" size={20} color="white" />
                  </View>
                  <View className="flex-1">
                    <Text className="text-gray-800 font-semibold">
                      {user.display_name}
                    </Text>
                    <Text className="text-gray-600 text-sm">
                      View memories
                    </Text>
                  </View>
                  <Ionicons name="chevron-forward" size={20} color="#6b7280" />
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        )}

        {searchResults.length === 0 && searchQuery && !searching && (
          <View className="bg-white p-6 rounded-lg border border-pink-200 shadow-sm">
            <View className="items-center">
              <Ionicons name="search-outline" size={48} color="#6b7280" />
              <Text className="text-gray-600 text-center mt-3 text-lg">
                No users found
              </Text>
              <Text className="text-gray-500 text-center mt-1">
                Try a different username or check the spelling
              </Text>
            </View>
          </View>
        )}
      </View>
    </View>
  );
}
