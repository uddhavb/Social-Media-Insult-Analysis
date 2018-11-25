import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class AbusiveWordsDetection {
	public static void main(String[] args) throws IOException{
		/*
		Map<Integer, Integer> abusive = new HashMap<Integer, Integer>();
		Map<Integer, Integer> nonAbusive = new HashMap<Integer, Integer>();
		*/
		int[][] abusiveOrNotArray = new int[2][11]; 
		BufferedReader br = new BufferedReader(new FileReader("Data.txt"));
	    String line;
	    int totalAbusive = 0;
	    int totalNonAbusive = 0;
	    while ((line = br.readLine()) != null) {
	    	String[] data = line.split("\\|");
	    	if(data.length<3)
	    		continue;
	    	int abusiveOrNot = Integer.parseInt(data[0]);
	    	String[] words = data[2].replaceAll("[^a-zA-Z ]", "").toLowerCase().split("\\s+");
	    	int invalidWordsCount = 0;
	    	for(String word: words){
	    		if(word==null||word.equals("")){
	    			continue;
	    		}
	    		boolean found = false;
	    		word = word.toLowerCase();
	    		
	    		if(word.charAt(0)>='a'&&word.charAt(0)<='g'){
	    			found = checkWordInFile("A-G.txt", word);
	    		}
	    		else if(word.charAt(0)>='h'&&word.charAt(0)<='n'){
	    			found = checkWordInFile("H-N.txt", word);
	    		}
	    		else if(word.charAt(0)>='o'&&word.charAt(0)<='t'){
	    			found = checkWordInFile("O-T.txt", word);
	    		}
	    		else if(word.charAt(0)>='u'&&word.charAt(0)<='z'){
	    			found = checkWordInFile("U-Z.txt", word);
	    		}
	    		if(!found)
	    			invalidWordsCount++;
	    	}
	    	/*if(abusiveOrNot == 1){
	    		if(abusive.containsKey(invalidWordsCount))
	    			abusive.put(invalidWordsCount, abusive.get(invalidWordsCount)+1);
	    		else
	    			abusive.put(invalidWordsCount, 1);
	    	}
	    	else{
	    		if(nonAbusive.containsKey(invalidWordsCount))
	    			nonAbusive.put(invalidWordsCount, nonAbusive.get(invalidWordsCount)+1);
	    		else
	    			nonAbusive.put(invalidWordsCount, 1);
	    	}*/
	    	invalidWordsCount = Math.min(10, invalidWordsCount);
	    	//System.out.println(invalidWordsCount+","+abusiveOrNot);
	    	if(abusiveOrNot == 1){
	    		totalAbusive++;
	    		abusiveOrNotArray[1][(int)invalidWordsCount]++;
	    	}
	    	else{
	    		totalNonAbusive++;
	    		abusiveOrNotArray[0][(int)invalidWordsCount]++;
	    	}
	    }
	 
	    int totalAbusiveWithInvalidWords = 0;
	    int totalNonAbusiveWithInvalidWords = 0;
	    for(int i=1;i<11;i++){
	    	totalAbusiveWithInvalidWords += abusiveOrNotArray[1][i];
	    	totalNonAbusiveWithInvalidWords += abusiveOrNotArray[0][i];
	    }
	    
	    System.out.println("Total documents = "+(totalAbusive+totalNonAbusive));
	    System.out.println("Total abusive = "+(totalAbusive));
	    System.out.println("Total non-abusive = "+(totalNonAbusive));
	    System.out.println("Total abusive with at least 1 invalid word = "+(totalAbusiveWithInvalidWords));
	    System.out.println("Total non-abusive with at least 1 invalid word = "+(totalNonAbusiveWithInvalidWords));
	    
	    System.out.println("Abusive: "+Arrays.toString(abusiveOrNotArray[1]));
	    System.out.println("Non-Abusive: "+Arrays.toString(abusiveOrNotArray[0]));
	    /*
	    System.out.println("Printing abusive");
	    for(int key: abusive.keySet()){
	    	System.out.println(key + "," + abusive.get(key));
	    }
	    System.out.println();
	    System.out.println("Printing non-abusive");
	    for(int key: nonAbusive.keySet()){
	    	System.out.println(key + "," + nonAbusive.get(key));
	    }*/
	}

	private static boolean checkWordInFile(String fileName, String word) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(fileName));
	    String line;
	    while ((line = br.readLine()) != null) {
	    	if(line.toLowerCase().equals(word))
	    		return true;
	    }
		return false;
	}
}
