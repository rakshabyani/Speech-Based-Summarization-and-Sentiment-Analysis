import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class MyCrawler extends WebCrawler {
	private final static Pattern FILTERS = Pattern.compile(".*(\\.(css|js|gif|jpg" + "|png|mp3|mp3|zip|gz))$");
	private final static Pattern RSS = Pattern.compile("\\/rss\\/");
	//private final static Pattern DORNSIFE = Pattern.compile("(http|https):.*dornsife.*.usc.edu.*");
	private final static Pattern NYTIMES = Pattern.compile("(http|https):.*youtube.com.*");
	private static int fileCtr = 0;

	/**
	 * This method receives two parameters. The first parameter is the page in
	 * which we have discovered this new url and the second parameter is the new
	 * url. You should implement this function to specify whether the given url
	 * should be crawled or not (based on your crawling logic). In this example,
	 * we are instructing the crawler to ignore urls that have css, js, git, ...
	 * extensions and to only accept urls that start with
	 * "http://www.viterbi.usc.edu/". In this case, we didn't need the
	 * referringPage parameter to make the decision.
	 */
	
	
	@Override
	public boolean shouldVisit(Page referringPage, WebURL url) {
		String href = url.getURL().toLowerCase();
		String desc = NYTIMES.matcher(href).matches() ? "OK" : "N_OK";
		writeUrlsCsv(href,desc);
		return (href.startsWith("http://youtube.com/") || href.startsWith("http://www.youtube.com/")); 
		//return !FILTERS.matcher(href).matches() && href.startsWith("http://www.nytimes.com/");
	}
	
	private void writeUrlsCsv(String href, String desc) {
		try
	    {
	        File urlsCsv = new File("../output/urls.csv");
	        if (!urlsCsv.exists()) 
	        {
	        	 urlsCsv.getParentFile().mkdirs();
	             urlsCsv.createNewFile();
	        }
	        
	        FileWriter fw = new FileWriter(urlsCsv.getAbsoluteFile(), true);
	        BufferedWriter bw = new BufferedWriter(fw);
            synchronized(this){
            	bw.write(href + ", " + desc + "\n");        // write to file
            }
	        bw.close();
	    }
	    catch (IOException e)
	    {
	        e.printStackTrace();
	    }
	}
	
	@Override
	protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
		writeFetchCsv(webUrl.getURL(), statusCode, statusDescription);
//		System.out.println("Url: " + webUrl.getURL() + " -- status: " + statusCode + " " + statusDescription);
		if(webUrl.getURL().endsWith("pdf")){
			System.out.println("PDF Url: " + webUrl.getURL() + " -- status: " + statusCode + " " + statusDescription);
		}
	}
	
	
	@Override
	 public void visit(Page page) {
		String url = page.getWebURL().getURL(); 
		System.out.println("Visit-url: " + url);
		
		String contentType = page.getContentType().split(";")[0];
		System.out.println("Content Type: " + contentType);
		System.out.println("Content data: " + page.getParseData().getOutgoingUrls());

		writeFiles(page);
		if(contentType != null && (contentType.contains("text/htm"))) {
			writeVisitCsv(url, page.getContentData().length, ((HtmlParseData) page.getParseData()).getOutgoingUrls().size(), page.getContentType());
			writePageRankData(url, (List<WebURL>) ((HtmlParseData) page.getParseData()).getOutgoingUrls());
		} /*else if(contentType.contains("application/pdf") || 
				contentType.contains("application/msword") || 
				contentType.contains("application/vnd.openxmlformats-officedocument.wordprocessingml.document")) {
			writeVisitCsv(url, page.getContentData().length, page.getParseData().getOutgoingUrls().size(), page.getContentType());
			writePageRankData(url, (List<WebURL>) (page.getParseData()).getOutgoingUrls());
			System.out.println("Entered--------------------------------------------------");
		}*/
		else {
			writeVisitCsv(url, page.getContentData().length, page.getParseData().getOutgoingUrls().size(), page.getContentType());
			writePageRankData(url, (List<WebURL>) (page.getParseData()).getOutgoingUrls());
		}
		
	}

/**
 * This function is called when a page is fetched and ready
 * to be processed by your program.
 */
	/* @Override
	* public void visit(Page page) {
	*	 String url = page.getWebURL().getURL();
	*	 System.out.println("URL: " + url);
	*	 System.out.println("HTTP Code : "+ page.getStatusCode());
	*	 if (page.getParseData() instanceof HtmlParseData) {
	*		 HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
	*		 String text = htmlParseData.getText();
	*		 String html = htmlParseData.getHtml();
	*		 Set<WebURL> links = htmlParseData.getOutgoingUrls();
	*		 System.out.println("Text length: " + text.length());
	*		 System.out.println("Html length: " + html.length());
	*		 System.out.println("Number of outgoing links: " + links.size());
	*	 }
	*}*/
	
	private void writeFiles(Page page) {
//		Document writing starts
		String contentType = page.getContentType().split(";")[0];
		String url = page.getWebURL().getURL(); 
		String fileName = url.replaceAll("/", "@");
		//System.out.println(contentType);
		//System.out.println(url);
		//System.out.println(fileName);
		try {
			FileOutputStream fos = new FileOutputStream("../output/docs/"+fileName);
			fos.write(page.getContentData());
			fileCtr++;
			if(fileCtr%100 == 0){
				System.out.println("Visit File Counter: " + fileCtr);
			}
			fos.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
//		document writing ends
	}
	
	private void writeFetchCsv(String webUrl, int statusCode, String statusDescription) {
		String url = webUrl;
		try
	    {
	        File fetch = new File("../output/fetch.csv");
	        if (!fetch.exists()) 
	        {
	        	 fetch.getParentFile().mkdirs();
	             fetch.createNewFile();
	        }
	        FileWriter fw = new FileWriter(fetch.getAbsoluteFile(), true);
	        BufferedWriter bw = new BufferedWriter(fw);
            synchronized(this){
            	bw.write(url + ", " + statusCode +"\n");        // write to file
            }
	        bw.close();
	    }
	    catch (IOException e)
	    {
	        e.printStackTrace();
	    }
	}
	
	private void writePageRankData(String url, List<WebURL> outgoingUrls) {
		try {

			File pageRankData = new File("../output/pagerank.csv");
			if (!pageRankData.exists()) {
				pageRankData.getParentFile().mkdirs();
				pageRankData.createNewFile();
			}
			FileWriter fwPageRank = new FileWriter(pageRankData.getAbsoluteFile(), true);
			BufferedWriter bwPageRank = new BufferedWriter(fwPageRank);

			bwPageRank.append(url); bwPageRank.append(',');
			if(outgoingUrls != null) {
				for (int i = 0; i < outgoingUrls.size(); i++) {
					WebURL u = outgoingUrls.get(i);
					bwPageRank.append(u.getURL());
					if (i != outgoingUrls.size() - 1)
						bwPageRank.append(',');
				}
			}
			bwPageRank.newLine();
			bwPageRank.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private void writeVisitCsv(String url, int fileSize, int outLinks, String pageType) {
		try
	    {
	        File file = new File("../output/visit.csv");
	       
	        if (!file.exists()) 
	        {
	        	 file.getParentFile().mkdirs();
	             file.createNewFile();
	        }
	        FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
	        BufferedWriter bw = new BufferedWriter(fw);
	    
            synchronized(this){
            	if(pageType.matches("text/html; charset=utf-8"))
            		pageType = "text/html";
            	if(pageType.matches("text/xml; charset=utf-8"))
            		pageType = "text/xml";
            	bw.write(url + ", " + fileSize + ", " + outLinks + ", " + pageType + "\n");        // write to file
            }
	        bw.close();
	    }
	    catch (IOException e)
	    {
	        e.printStackTrace();
	    }
		
	}
}
