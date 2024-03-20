function TopicsPage() {
    return (
        <>
            <h2>Web Development Concepts</h2>
            <nav class="local">
                <a href="#webServers">Web Servers</a>
                <a href="#frontendDesign">Frontend Design</a>
                <a href="#optimisingImages">Optimizing Images</a>
            </nav>
                <article id="webServers">
                    <h3>Web Servers</h3>
                    <p>The base HTML file, <strong>index.html</strong>, is the default designated home page for a given website and/or web server, and is referenced when a request is given for '/'. Web servers can have different default home pages, such as <strong>default.html</strong> with .NET, but OSU's Apache server uses index.html.</p>
                    <p>In the <strong>network tab</strong> of a browser's inspector, there are three main sections: <strong>General</strong>, including request information -- <strong>Response Headers</strong>, including response information -- and <strong>Request Headers</strong>, including request specifics such as method, scheme, user-agent, and more.
                        Specifically in general, HTML requests, including the request URL, the request method, the status code, and potentially the IP address, is displayed.
                        Under response headers, cache age, data regarding the server's status such as 'AmazonS3', date, and other relevant information is displayed.
                        Under request headers, specifics of the request are displayed, including method, scheme, path, browser information user-agent, origin, and more.
                        When comparing the locally hosted page to the Apache hosted page, the way the COE server is different is that it has a remote address, displays information like cache age, server time, and other server info, and extensive request information, including <strong>host info</strong> and more.
                        On the other hand, the locally hosted page simply displayed the request URL, method, and status code, as well as the content type and basic user info--windows, chrome--, omitting almost all the server request and response information.
                    </p>
                    <p>Because the OSU COE server already has a <strong>favicon.ico</strong> file for students to use, it was able to be retrieved by the <strong>HTML request</strong>, and as such returns a <strong>status code of 200</strong> for OK.
                        However, as we did not create or upload CSS or JS files, they were not able to be retrieved by the <strong>HTML request</strong>, and therefore returned <strong>400 status codes</strong>, which indicates the client's request failed.
                    </p>
                    <p>On the website hosted on the COE server, the segment 'https://' is the <strong>protocol/scheme</strong>, 'web.engr' is the <strong>subdomain</strong>, 
                        'oregonstate.edu' is the <strong>domain</strong>, and the <strong>resource</strong> is the file 'a1-dobkinr' in the directory '~dobkinr/'.</p>
                </article>
            <article id="frontendDesign">
                <h3>Frontend Design</h3>
                <p><strong>Frontend design</strong> is the concept of designing a user interface that is appealing, effective, efficient, and accessible, and allows the user to use your site to fulfill their needs.
                    This can include appropriate and accessible use of color and fonts, media that is optimized for both speed and SEO and compatible with screen readers, implicitly understandable user interface with navigation options, appealing icons, and more.
                </p>
                <p>The five E's of good frontend design are:</p>
                <dl>
                    <strong><dt>Effective</dt></strong>
                    <dd>User is able to meet their goal(s).</dd>
                    <strong><dt>Efficient</dt></strong>
                    <dd>Users can perform tasks in the least number of steps.</dd>
                    <strong><dt>Easy to Navigate</dt></strong>
                    <dd>Users are able to understand how to locate their goal immediately.</dd>
                    <dd>Intuitive to new users.</dd>
                    <strong><dt>Error-free</dt></strong>
                    <dd>Users should not experience accessibility or availability errors.</dd>
                    <strong><dt>Enjoyable; Engaging</dt></strong>
                    <dd>Users needs are fulfilled in content and design.</dd>
                </dl>
                <p>The six-page layout tags we covered include: <strong>header, nav, main, section, article, and footer</strong>.
                    <strong>Header</strong> designated the beginning of a section of content, and in my case, is defined as 'Ryan Dobkin' at the beginning of the body, acting as a banner.
                    <strong>Nav</strong> designates a navigation section of the page that can be used to access other pages, sections of the current page, or outside web pages.
                    <strong>Main</strong> designates the content that will appear in the browser's viewport.
                    <strong>Section</strong> designated a dedicated but independent area of the document. It has a header and potentially contains articles.
                    <strong>Articles</strong> are typically subsections or act as a specific container that contain second-level headings.
                    <strong>Footer</strong> designates the bottom of a webpage. It is typically where critical pages, or legal/contact information is displayed, often including copyright information.
                </p>
                <p>The three ways anchors can be used to link to external, internal, and related pages together are:</p>
                <ol>
                    <li>To reference external content, <strong>Anchors</strong> create hyperlinks to the website referenced via its href attribute.</li>
                    <li><strong>Anchors</strong> can link to internal content by referencing a section, using a # in front of the section id in the href attribute.</li>
                    <li><strong>Anchors</strong> can link page-to-page by referencing the directory of the new page in the href. For example, if the file contacts.html is in the same directory as index.html, simply referencing contacts.html in the href will bring you to the new page.</li>
                </ol>
            </article>
            <article id="optimisingImages">
                <h3>Optimizing Images for the Web</h3>
                <p>When optimizing for the web, there are 6 major specifications that should be followed. (1) The images should have descriptive files names to improve SEO, 
                    (2) have small file sizes to load fast on all devices, only serving high quality variants to high resolution devices, (3) and fit the exact dimensions in which it will be displayed to load efficiently.
                    (4) Images for the web should also have the correct file format, typically .JPG but also .GIF or .PNG for line-art, icons, or graphics. (5) When possible,
                    images should also provide a range of images varying from 72ppi to 300ppi+ in order to serve all devices appropriately and efficiently. (6) Finally, images should follow
                    the correct color mode for their format, with RGB being used for .PNG, .JPG, .SVG, and .WebP, and Indexed for .GIF, and sometimes .PNG.
                </p>
                <p>
                    For photos, the most appropriate file format is .JPG or WebP, and for line art, .PNG, .SVG, or .GIF is the most appropriate. For photos, 
                    because they will often have very high file size, making it a .JPG or .WebP will significantly reduce the file size so that it is appropriate to display on the web, with the tradeoff of lost quality.
                    The reason .PNG, .SVG, or .GIF are used for line art is because they all have true transparency options. They also allow for animation and low loss compression, and in the case of .SVG, offer compression
                    based on vector graphics, leaving almost no compression artifacts.
                </p>
                <p>
                    Favicons are used to help users easily associate links or tabs with a website.
                    They can be displayed as shortcuts on handheld devices, bookmarks, or tab indicators on browsers, and otherwise act as easy identifiers for a given website.
                </p>
            </article>
        </>
    );
}

export default TopicsPage;