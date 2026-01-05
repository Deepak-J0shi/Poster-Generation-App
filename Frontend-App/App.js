import React, { useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  ScrollView,
  Alert,
  Platform,
  StyleSheet,
} from "react-native";
import * as FileSystem from "expo-file-system/legacy";
import * as Sharing from "expo-sharing";
import { encode as btoa } from "base-64";
import { LinearGradient } from "expo-linear-gradient";

/* API endpoint (keep your IP) */
const API_URL = "http://10.143.26.188:8000/generate";

export default function App() {
  const [salonName, setSalonName] = useState("");
  const [offer, setOffer] = useState("");
  const [loading, setLoading] = useState(false);
  const [posterUri, setPosterUri] = useState(null);

  async function submit() {
    if (!salonName.trim()) {
      Alert.alert("Validation", "Salon / Brand name is required.");
      return;
    }

    setLoading(true);
    setPosterUri(null);
    try {
      const form = new FormData();
      form.append("salonName", salonName);
      form.append("offer", offer || "");

      const response = await fetch(API_URL, { method: "POST", body: form });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Server error: ${response.status} ${text}`);
      }

      const arrayBuffer = await response.arrayBuffer();
      const base64 = bufferToBase64(arrayBuffer);

      const filename = FileSystem.cacheDirectory + `poster_${Date.now()}.png`;
      await FileSystem.writeAsStringAsync(filename, base64, { encoding: "base64" });

      setPosterUri(filename);
    } catch (err) {
      console.error(err);
      Alert.alert("Error", err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function bufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = "";
    const chunkSize = 0x8000;
    for (let i = 0; i < bytes.length; i += chunkSize) {
      binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunkSize));
    }
    return btoa(binary);
  }

  async function sharePoster() {
    if (!posterUri) return;
    try {
      if (!(await Sharing.isAvailableAsync())) {
        Alert.alert("Sharing not supported on this device");
        return;
      }
      await Sharing.shareAsync(posterUri);
    } catch (err) {
      Alert.alert("Share error", err.message);
    }
  }

  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.scroll}>
        {/* Top header banner (small) */}
        <View style={styles.topBanner}>
          <View style={styles.logoCircle}>
            {/* small icon: you can replace with an asset image if you want */}
            <Text style={styles.logoEmoji}>✨</Text>
          </View>
          <View style={styles.bannerText}>
            <Text style={styles.bannerTitle}>Glownify Poster Studio</Text>
            <Text style={styles.bannerSub}>Auto-generate salon posters in seconds.</Text>
          </View>
        </View>

        {/* Card with form */}
        <View style={styles.card}>
          <Text style={styles.label}>Salon / Brand Name *</Text>
          <TextInput
            style={styles.input}
            value={salonName}
            onChangeText={setSalonName}
            placeholder="Glownify Beauty Lounge"
            placeholderTextColor="#9aa0a6"
          />

          <Text style={styles.label}>Offer / Tagline</Text>
          <TextInput
            style={styles.input}
            value={offer}
            onChangeText={setOffer}
            placeholder="Flat 30% off on festive makeovers"
            placeholderTextColor="#9aa0a6"
          />

          <TouchableOpacity activeOpacity={0.9} onPress={submit} style={styles.buttonWrapper}>
            <LinearGradient colors={["#ff8a00", "#d61eff"]} start={[0,0]} end={[1,1]} style={styles.gradient}>
              {loading ? <ActivityIndicator color="white" /> : <Text style={styles.buttonText}>Generate Poster ⚡</Text>}
            </LinearGradient>
          </TouchableOpacity>

          <Text style={styles.hint}>After generating, the poster will appear below. Use Share to save.</Text>
        </View>

        {/* Poster preview area */}
        {posterUri && (
          <View style={styles.result}>
            <Text style={styles.resultTitle}>Generated Poster:</Text>
            <Image source={{ uri: posterUri }} style={styles.poster} />
            <TouchableOpacity style={styles.shareBtn} onPress={sharePoster}>
              <LinearGradient colors={["#06b6d4", "#3b82f6"]} style={styles.smallGradient}>
                <Text style={styles.shareText}>Share / Save</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#0f1724" },
  scroll: { padding: 18, alignItems: "center", paddingBottom: 60,  marginTop: 40 },

  topBanner: {
    width: "100%",
    maxWidth: 840,
    backgroundColor: "#0b1220",
    borderRadius: 12,
    padding: 10,
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 18,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.03)",
    shadowColor: "#000",
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  logoCircle: {
    width: 44,
    height: 44,
    borderRadius: 44,
    backgroundColor: "#2b2f6b",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
  },
  logoEmoji: { fontSize: 22 },
  bannerText: { flex: 1 },
  bannerTitle: { color: "#fff", fontSize: 16, fontWeight: "700" },
  bannerSub: { color: "#9fb0c8", fontSize: 12, marginTop: 2 },

  card: {
    width: "100%",
    maxWidth: 840,
    backgroundColor: "#0b1220",
    borderRadius: 14,
    padding: 18,
    shadowColor: "#000",
    shadowOpacity: 0.4,
    shadowRadius: 10,
    elevation: 8,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.03)",
  },

  label: { color: "#cbd5e1", fontSize: 13, marginTop: 8, marginBottom: 6 },
  input: {
    backgroundColor: "#0b1228",
    color: "#fff",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.03)",
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderRadius: 10,
    fontSize: 15,
  },

  buttonWrapper: { marginTop: 16, borderRadius: 12, overflow: "hidden" },
  gradient: { paddingVertical: 14, alignItems: "center", justifyContent: "center", borderRadius: 12 },
  buttonText: { color: "#fff", fontWeight: "700", fontSize: 16 },

  hint: { color: "#98a0ac", marginTop: 12, fontSize: 12 },

  result: { width: "100%", maxWidth: 840, marginTop: 20, alignItems: "center" },
  resultTitle: { color: "#e6eef8", alignSelf: "flex-start", marginBottom: 8, fontSize: 15, fontWeight: "600" },
  poster: { width: "100%", aspectRatio: 9 / 16, borderRadius: 8, borderWidth: 1, borderColor: "rgba(255,255,255,0.04)", backgroundColor: "#fff" },

  shareBtn: { marginTop: 12, borderRadius: 10, overflow: "hidden" },
  smallGradient: { paddingVertical: 10, paddingHorizontal: 24, borderRadius: 10 },
  shareText: { color: "#fff", fontWeight: "700" },
});
