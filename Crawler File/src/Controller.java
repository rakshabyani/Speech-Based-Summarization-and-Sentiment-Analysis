import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Scanner;

import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

public class Controller {
	public static void main(String[] args) throws Exception {
		 String crawlStorageFolder = "/data/crawl";
		 int numberOfCrawlers = 10;
		 
		 CrawlConfig config = new CrawlConfig();
		 config.setCrawlStorageFolder(crawlStorageFolder);
		 config.setMaxDepthOfCrawling(16);
		 config.setMaxPagesToFetch(20000);
		 config.setIncludeBinaryContentInCrawling(true);
		 
		 //config.setPolitenessDelay(500);
		 
		 
		 /*
		 * Instantiate the controller for this crawl.
		 */
		 PageFetcher pageFetcher = new PageFetcher(config);
		 RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
		 RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
		 CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);
		 /*
		 * For each crawl, you need to add some seed urls. These are the first
		 * URLs that are fetched and then the crawler starts following links
		 * which are found in these pages
		 */	
		 deleteOldFiles();
		 controller.addSeed("https://www.youtube.com/watch?v=2pRMp17m9m4");
		 /*
		 * Start the crawl. This is a blocking operation, meaning that your code
		 * will reach the line after this only when crawling is finished.
		 */

		 controller.start(MyCrawler.class, numberOfCrawlers);
		
		 
		 writeCrawlReport();
		 System.out.println("Program terminates.....");
	}

	private static void writeCrawlReport() {
		// TODO Auto-generated method stub
		try {
			File crawlReport = new File("../output/CrawlReport.txt");
			if (crawlReport.exists()) {
				crawlReport.delete();
			} else {
				crawlReport.getParentFile().mkdirs();
				crawlReport.createNewFile();
			}
			FileWriter fw = new FileWriter(crawlReport.getAbsoluteFile(), true);
			BufferedWriter bw = new BufferedWriter(fw);
			String splitby = ", ";

			bw.append("Name: Paridhi Verma");
			bw.newLine();
			bw.append("USC ID: 5333348251");
			bw.newLine();
			bw.append("News Site crawled: NY_Times");
			bw.newLine();
			
			File fetchCsv = new File("../output/fetch.csv");
			if (fetchCsv.exists()) {
				Scanner inputStream;
				int fetchAttempt = 0, fetchSuccess = 0, fetchFailed = 0, fetchAborted = 0;
				HashMap<String, Integer> statusCodes = new HashMap<String, Integer>();
				try {
					inputStream = new Scanner(fetchCsv);

					while (inputStream.hasNext()) {
						String data = inputStream.nextLine();
						String a[] = data.split(splitby);
						if (statusCodes.get(a[1]) != null) {
							statusCodes.put(a[1], statusCodes.get(a[1]) + 1);
						} else {
							statusCodes.put(a[1], 1);
						}
					}
					
					HashMap<String, String> codeDesc = new HashMap<String, String>();
					codeDesc.put("302", "Moved Temporarily");
					codeDesc.put("1001", "Page size was too big");
					codeDesc.put("303", "See Other");
					codeDesc.put("301", "Moved Permanently");
					codeDesc.put("200", "OK");
					codeDesc.put("1005", "Fatal transport error");
					codeDesc.put("404", "Not Found");
					codeDesc.put("403", "Forbidden");
					codeDesc.put("405", "Method Not Allowed");
					codeDesc.put("503", "Service Unavailable");
					codeDesc.put("500", "Internal Server Error");
					codeDesc.put("400", "Bad Request");
					codeDesc.put("410", "Gone");

					bw.newLine();
					bw.append("Status Codes:");
					bw.newLine();
					bw.append("=============");
					bw.newLine();

					for (Iterator i = statusCodes.keySet().iterator(); i.hasNext();) {
						String key = (String) i.next();
						Integer value = statusCodes.get(key);
						
						switch(key.charAt(0)) {
							case '2' : fetchSuccess += value; break;
							case '3' : fetchAborted += value; break;
							default  : fetchFailed += value; break;
						}
						if(codeDesc.get(key)!=null){
							key = key + " " + codeDesc.get(key);
						}
						
						bw.append(key + " = " + value);
						bw.newLine();
					}
					
					fetchAttempt = fetchSuccess + fetchAborted + fetchFailed;
					
					bw.newLine();
					bw.append("Fetch Statistics");
					bw.newLine();
					bw.append("================");
					bw.newLine();
					bw.append("# fetches attempted: " + fetchAttempt);
					bw.newLine();
					bw.append("# fetches succeeded: " + fetchSuccess);
					bw.newLine();
					bw.append("# fetches aborted: " + fetchAborted);
					bw.newLine();
					bw.append("# fetches failed: " + fetchFailed);
					bw.newLine();
					System.out.println("Fetch.csv complete!!");
					inputStream.close();
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				}
			}

			File urlsCsv = new File("../output/urls.csv");
			int inNewsSite=0, outNewsSite=0, totalUrl=0;
			HashSet<Object> uniqueUrlSet = new HashSet<Object>();
			if (urlsCsv.exists()) {
				Scanner inputStream = new Scanner(urlsCsv);
				while (inputStream.hasNext()) {
					totalUrl++;
					String data = inputStream.nextLine();
					String a[] = data.split(splitby);
					if(uniqueUrlSet.add(a[0])) {
						switch (a[1]) {
						case "OK":
							inNewsSite++;
							break;
						case "N_OK":
							outNewsSite++;
							break;
						}
					}
				}
				bw.newLine();
				bw.append("Outgoing URLs:");
				bw.newLine();
				bw.append("==============");
				bw.newLine();
				bw.append("Total URLs extracted: " + totalUrl);
				bw.newLine();
				bw.append("# unique URLs extracted: " + uniqueUrlSet.size());
				bw.newLine();
				bw.append("# unique URLs within News Site: " + inNewsSite);
				bw.newLine();
				bw.append("# unique USC URLs outside News Site: " + outNewsSite);
				bw.newLine();
				System.out.println("Url.csv complete!!");
				inputStream.close();
			}
			
			File visitCsv = new File("../output/visit.csv");
			int checkByteSize;
			String key;
			int s1kb = 0;
			int s1to10kb = 0;
			int s10to100kb = 0; 
			int s1000to1mb = 0;
			int sGreaterThan1mb = 0;
			HashMap<String, Integer> contentTypeMap = new HashMap<>();
			if (visitCsv.exists()) {
				Scanner inputStream = new Scanner(visitCsv);
				bw.newLine();
				
				while(inputStream.hasNext()){
					String data = inputStream.nextLine();
					String a[] = data.split(splitby);
//					System.out.println(a[1] + ", " + a[3].split(";")[0]);
//					System.out.println("Int value: " + Integer.parseInt(a[1]));
					
					checkByteSize = Integer.parseInt(a[1]);
					if(checkByteSize < 1024) {
						s1kb++;
					} else if(1024 <= checkByteSize && checkByteSize < 10240) {
						s1to10kb++;
					} else if(10240 <= checkByteSize && checkByteSize < 102400) {
						s10to100kb++;
					} else if(102400 <= checkByteSize && checkByteSize < 1048576) {
						s1000to1mb++;
					} else {
						sGreaterThan1mb++;
					}
					key = a[3].split(";")[0];
					if(contentTypeMap.get(key) != null){
						contentTypeMap.put(key, contentTypeMap.get(key)+1);
					} else {
						contentTypeMap.put(key, 1);
					}
				}
				
				bw.append("File Sizes:"); bw.newLine();
				bw.append("==========="); bw.newLine();
				bw.append("<1kb: " + s1kb); bw.newLine();
				bw.append("1kb ~ 10kb: " + s1to10kb); bw.newLine();
				bw.append("10kb ~ 100kb: " + s10to100kb); bw.newLine();
				bw.append("100kb ~ 1mb: " + s1000to1mb); bw.newLine();
				bw.append(">= 1mb: " + sGreaterThan1mb); bw.newLine();

				bw.newLine();
				bw.append("Content Types:"); bw.newLine();
				bw.append("=============="); bw.newLine();
				
				for (Iterator i = contentTypeMap.keySet().iterator(); i.hasNext();) {
					String contentType = (String) i.next();
					Integer value = contentTypeMap.get(contentType);
					bw.append(contentType + ": " + value); bw.newLine();
				}
				
				inputStream.close();
			}
			bw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Go check! ;)");
	}

	private static void deleteOldFiles() {
		// TODO Auto-generated method stub
		File visitCsv = new File("../output/visit.csv");
        if (visitCsv.exists()) 
        {
        	 visitCsv.delete();
        }
        File urlsCsv = new File("../output/urls.csv");
        if (urlsCsv.exists()) 
        {
        	urlsCsv.delete();
        }
        File fetchCsv = new File("../output/fetch.csv");
        if (fetchCsv.exists()) 
        {
        	fetchCsv.delete();
        }
        File pageRankDataCsv = new File("../output/pagerank.csv");
        if (pageRankDataCsv.exists()) 
        {
        	pageRankDataCsv.delete();
        }
        System.out.println("All files deleted.");
	}

}
