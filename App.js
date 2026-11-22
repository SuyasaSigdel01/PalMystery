import { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, TextInput, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const API_URL = 'http://192.168.1.64:8000';

const Tab = createBottomTabNavigator();

function Placeholder({ title }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <StatusBar style="auto" />
    </View>
  );
}

function HomeScreen() {
  return <Placeholder title="Home" />;
}

function ScanScreen() {
  return <Placeholder title="Scan" />;
}

function ReadingsScreen() {
  return <Placeholder title="Readings" />;
}

function ProfileScreen() {
  return <Placeholder title="Profile" />;
}

function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function handleLogin() {
    setBusy(true);
    setError('');
    try {
      const res = await fetch(API_URL + '/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, password: password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || 'Login failed');
        return;
      }
      onLogin(data.token);
    } catch (err) {
      setError('Cannot reach server');
    } finally {
      setBusy(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>PalMystery</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title={busy ? 'Please wait' : 'Log in'} onPress={handleLogin} disabled={busy} />
      <Text style={styles.error}>{error}</Text>
      <StatusBar style="auto" />
    </View>
  );
}

export default function App() {
  const [token, setToken] = useState(null);

  if (!token) {
    return <LoginScreen onLogin={setToken} />;
  }

  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Scan" component={ScanScreen} />
        <Tab.Screen name="Readings" component={ReadingsScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 24,
    marginBottom: 24,
  },
  input: {
    width: '100%',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 6,
    padding: 12,
    marginBottom: 12,
  },
  error: {
    color: '#c00',
    marginTop: 12,
  },
});
