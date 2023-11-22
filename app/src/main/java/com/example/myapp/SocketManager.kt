package com.example.myapp

import android.util.Log
import io.socket.client.IO
import io.socket.client.Socket
import io.socket.emitter.Emitter

object SocketManager {
    private var mSocket: Socket? = null

    fun setSocket(socket: Socket) {
        mSocket = socket
        setupSocketEvents()
    }

    private fun setupSocketEvents() {
        mSocket?.on(Socket.EVENT_CONNECT) {
            Log.d("SocketManager", "Connected to server")
        }?.on(Socket.EVENT_DISCONNECT) {
            Log.d("SocketManager", "Disconnected from server")
        }?.on(Socket.EVENT_CONNECT_ERROR) { args ->
            Log.e("SocketManager", "Connection error: ${args[0]}")
        }
    }

    fun getSocket(): Socket? {
        return mSocket
    }

    fun connect() {
        mSocket?.connect()
    }

    fun disconnect() {
        mSocket?.disconnect()
    }
}
