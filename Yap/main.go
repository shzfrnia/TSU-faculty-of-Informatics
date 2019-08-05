package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"time"
)

func main() {
	rand.Seed(int64(time.Now().Second()))
	var port string
	flag.StringVar(&port, "port", "8080", "Port for TCP")
	modePtr := flag.String("mode", "S", "Application mode")
	flag.Parse()
	fmt.Println("My mode is: " + *modePtr)
	switch *modePtr {
	case "S":
		listenClient(port)
	case "C":
		dialServer(port)
	default:
		fmt.Println("Mode" + *modePtr + "is not exists")
	}

	//  Кей не следущей это кей с предыдущей ТЕСТЫ
	// hashString := "01234"
	// sessionKey := "0123456789"
	// protectorClient := sessionProtector{hash: hashString}
	// protectorServer := sessionProtector{hash: hashString}
	// for i := 0; i < 10; i++ {
	// 	temp, _ := protectorClient.nextSessionKey(sessionKey)
	// 	temp2, _ := protectorServer.nextSessionKey(sessionKey)
	// 	if temp == temp2 {
	// 		// fmt.Println("Passed")
	// 		fmt.Println(temp)
	// 		sessionKey = temp
	// 	} else {
	// 		fmt.Println("Error")
	// 	}
	// }

	// fmt.Println(GetSessionKey())
	// fmt.Println(GetHashStr())
	// pr := SessionProtector{hash: "12345"} // TODO 4 одинаковые цифры вызфвают паник
	// fmt.Println("case 1")
	// fmt.Println(pr.calcHash("123456", 1))
	// fmt.Println("case 2")
	// fmt.Println(pr.calcHash("123456", 2))
	// fmt.Println("case 3")
	// fmt.Println(pr.calcHash("123456", 3))
	// fmt.Println("case 4")
	// fmt.Println(pr.calcHash("123456789", 4))
	// fmt.Println("case 5")
	// fmt.Println(pr.calcHash("123456789", 5))
	// fmt.Println("***********")
	// fmt.Println(pr.NextSessionKey("123456789"))
}

func dialServer(port string) {
	conn, err := net.Dial("tcp", "localhost:"+port)
	if err != nil {
		panic("Error")
	}

	clientHash := getHashStr()
	clientSKey := getSessionKey()
	var sKey string
	protector := sessionProtector{hash: clientHash}

	for i := 0; i < 5; i++ {
		if sKey == "" {
			sKey = clientSKey
			textToServer := clientHash + " " + clientSKey
			fmt.Fprint(conn, textToServer+"\n")
		} else {
			sKey, _ = protector.nextSessionKey(sKey)
			fmt.Fprintf(conn, sKey+"\n")
		}
		message, _ := bufio.NewReader(conn).ReadString('\n')
		message = message[:len(message)-1]
		sKey, _ = protector.nextSessionKey(sKey)
		fmt.Println("My key: " + sKey)
		if message != sKey {
			panic("Diffirent keys")
		}
		fmt.Println("Passed")
	}
	conn.Close()
}

func listenClient(port string) {
	fmt.Println("Launching server...")
	var protector sessionProtector

	// listen on all interfaces
	ln, err := net.Listen("tcp", ":"+port)
	if err != nil {
		panic("Error launch server")
	}
	for {
		conn, err := ln.Accept()
		fmt.Println("Client connect")
		if err != nil {
			panic("panic")
		}
		go handleConnection(conn, protector)
	}
}

func handleConnection(conn net.Conn, protector sessionProtector) {
	for {
		// will listen for message to process ending in newline (\n)
		message, _ := bufio.NewReader(conn).ReadString('\n')
		if len(message) == 0 {
			fmt.Println("Client disconnect")
			conn.Close()
			return
		}
		message = message[:len(message)-1]
		// sample process for string received
		// newmessage := strings.ToUpper(message)
		// // send new string back to client
		fmt.Println("Message Received: " + string(message)) //output message
		var clientSkey, clientHash string
		if strings.Contains(message, " ") {
			temp := strings.Split(message, " ")
			clientHash = temp[0]
			clientSkey = temp[1]
			protector = sessionProtector{hash: clientHash}
		} else {
			clientSkey = message
		}
		sKey, _ := protector.nextSessionKey(clientSkey)
		fmt.Println("Session Key:" + sKey)
		conn.Write([]byte(sKey + "\n"))
	}
}

// Generate random string 10 len
func getSessionKey() (result string) {
	result = ""
	for i := 0; i < 10; i++ {
		result += string(int('a') + rand.Intn(26))
	}
	return
}

//Generate random string 5 len
func getHashStr() (result string) {
	result = ""
	for i := 0; i < 5; i++ {
		result += strconv.Itoa(rand.Intn(10))
	}
	return
}

type sessionProtector struct {
	hash string
}

func (protector sessionProtector) nextSessionKey(sessionKey string) (string, error) {
	if protector.hash == "" {
		return "", errors.New("Hash code is empty")
	}
	for idx := 0; idx < len(protector.hash); idx++ {
		i := protector.hash[idx]
		if _, err := strconv.Atoi(string(i)); err != nil {
			return "", errors.New("Hash code contains non-digit letter")
		}
	}
	result := 0
	var temp int
	var buffer string
	var err error
	for idx := 0; idx < len(protector.hash); idx++ {
		i := int(protector.hash[idx])
		temp, err = strconv.Atoi(string(i))
		buffer, err = protector.calcHash(sessionKey, temp)
		temp, err = strconv.Atoi(buffer)
		result += temp
	}
	buffer = strconv.Itoa(result)
	zeros := "0000000000"
	buffer = zeros + buffer[:len(buffer)]
	return buffer[len(buffer)-10:], err
}

func (protector sessionProtector) calcHash(sessionKey string, val int) (string, error) {
	result := ""
	switch val {
	case 1:
		temp, err := strconv.Atoi(sessionKey[:5])
		result = "00" + strconv.Itoa(temp%97)
		return (result)[len(result)-2:], err
	case 2:
		for i := len(sessionKey) - 1; i >= 0; i-- {
			result += string(sessionKey[i])
		}
		return result, nil
	case 3:
		for i := len(sessionKey) - 5; i < len(sessionKey); i++ {
			result += string(sessionKey[i])
		}
		for i := 0; i < 5; i++ {
			result += string(sessionKey[i])
		}
		return result, nil
	case 4:
		num := 0
		temp, err := 0, errors.New("Zero iterations")
		for i := 1; i < 9; i++ {
			temp, err = strconv.Atoi(string(sessionKey[i]))
			num += temp + 41
		}
		result = strconv.Itoa(num)
		return result, err
	case 5:
		num := 0
		var err error
		var temp int
		for i := 0; i < len(sessionKey); i++ {
			ch := sessionKey[i] ^ 43
			if _, err = strconv.Atoi(string(ch)); err != nil {
				temp = int(ch)
			}
			num += temp
		}
		result = strconv.Itoa(num)
		return result, nil
	default:
		temp, err := strconv.Atoi(sessionKey)
		temp = temp + val
		result = strconv.Itoa(temp)
		return result, err
	}
}
