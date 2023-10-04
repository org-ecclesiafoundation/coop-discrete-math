package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"math/big"
	"os"
	"strconv"
)

func main() {
	heterogramsJson := os.Args[1]
	difficulty, difficultyErr := strconv.Atoi(os.Args[2])
	if difficultyErr != nil {
		panic(difficultyErr)
	}
	countsLengths := os.Args[3:]
	var counts []int
	var lengths []int
	for idx := 0; idx < len(countsLengths); idx += 2 {
		c, cErr := strconv.Atoi(countsLengths[idx])
		l, lErr := strconv.Atoi(countsLengths[idx])
		if cErr != nil || lErr != nil {
			panic("error converting counts and lengths")
		}
		counts = append(counts, c)
		lengths = append(lengths, l)
	}
	fmt.Printf("Counts: %d\n", counts)
	fmt.Printf("Lengths: %d\n", counts)

	data, fileReadErr := os.Open(heterogramsJson)
	if fileReadErr != nil {
		panic(fileReadErr)
	}

	heterogramsData, dataReadErr := io.ReadAll(data)
	if dataReadErr != nil {
		panic(dataReadErr)
	}

	var heterograms map[string][]string
	unmarshalErr := json.Unmarshal(heterogramsData, &heterograms)
	if unmarshalErr != nil {
		fmt.Println("in unmarshalling")
		panic(unmarshalErr)
	}

	var words []string
	for _, length := range lengths {
		for _, count := range counts {
			word := heterograms[strconv.Itoa(length)][count]
			words = append(words, word)
		}
	}

	var problems []string
	for _, word := range words {
		problems = append(problems, GenerateProblem(difficulty, word))
	}
	for _, problem := range problems {
		fmt.Println(problem)
	}
}

func GenerateProblem(difficulty int, word string) string {
	wordLetters := make(map[rune]struct{})
	setA := make(map[rune]struct{})
	setB := make(map[rune]struct{})
	for _, letter := range word {
		_, exists := wordLetters[letter]
		if exists {
			panic("word " + word + " is not a heterogram")
		}
		wordLetters[letter] = struct{}{}
		setA[letter] = struct{}{}
		setB[letter] = struct{}{}
	}
	chars := []rune{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
		'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
	nums := []rune{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

	if 26 < (difficulty + len(word)) {
		for _, num := range nums {
			chars = append(chars, num)
		}
	}

	shuffledChars := shuffle(chars)

	whichSet := false
	addedChars := 0
	for _, char := range shuffledChars {
		if difficulty < addedChars {
			break
		}
		if whichSet {
			_, exists := setA[char]
			if !exists {
				setA[char] = struct{}{}
				addedChars++
			}
		} else {
			_, exists := setB[char]
			if !exists {
				setB[char] = struct{}{}
				addedChars++
			}
		}
		whichSet = !whichSet
	}
	strA := "Set A: "
	strB := "Set B: "
	for key := range setA {
		strA = strA + " " + string(key)
	}
	for key := range setB {
		strB = strB + " " + string(key)
	}
	return fmt.Sprintf("%s\n  %s\n  %s", word, strA, strB)
}

func shuffle(data []rune) []rune {
	n := len(data)
	result := make([]rune, n)
	copy(result, data)

	for i := n - 1; i > 0; i-- {
		j, _ := rand.Int(rand.Reader, big.NewInt(int64(i+1)))
		result[i], result[j.Int64()] = result[j.Int64()], result[i]
	}
	return result
}
