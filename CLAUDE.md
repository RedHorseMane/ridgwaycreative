# Claude Code Changes Log

## 2025-11-28 - Bilingual Site Implementation

### Changes Made:
1. **Fixed Navigation Links**
   - Navigation bar links at top right were incorrectly pointing to privacy policy pages
   - Updated to toggle between English and French versions of the site content

2. **Added Bilingual Support**
   - Implemented single-page app with English/French language toggle
   - All content now available in both languages within index.html
   - JavaScript toggles language without page reload
   - Language preference stored in localStorage

3. **Technical Implementation**
   - Added `data-lang-en` and `data-lang-fr` attributes to translatable elements
   - Created `toggleLanguage()` function to switch between languages
   - Updated HTML lang attribute dynamically
   - Maintained single-page app architecture

### Files Modified:
- `index.html` - Added bilingual content and language toggle functionality
- `CLAUDE.md` - Created this change log

### Future Considerations:
- Consider adding more languages if needed
- Could extract translations to separate JSON files for easier management
- May want to add language detection based on browser preferences

---

## 2025-11-28 - Security and SEO Improvements

### Changes Made:
1. **robots.txt Updates**
   - Uncommented sitemap directive to enable sitemap.xml discovery
   - Added disallow rules for internal-use social media redirect pages (bluesky.html, facebook.html, instagram.html, threads.html)
   - Maintained existing crawl-delay for bingbot and folder exclusions

2. **_headers Security Enhancements**
   - Added Content-Security-Policy (CSP) header with appropriate allowlists for:
     - Google Analytics (www.googletagmanager.com)
     - Klaro cookie consent (cdn.kiprotect.com)
     - External APIs (bradyridgway.pythonanywhere.com, api.adviceslip.com)
     - Geolocation service (ipapi.co)
   - Added X-XSS-Protection header for legacy browser protection
   - Improved caching strategy:
     - /static/* assets now use long-term caching (1 year) with immutable flag
     - CSS/JS files now cache for 1 week (was 0) to improve performance while supporting versioning
   - Maintained existing CORS, HSTS, and other security headers

### Files Modified:
- `robots.txt` - Added sitemap directive and social media page exclusions
- `_headers` - Enhanced security headers and caching strategy
- `CLAUDE.md` - Updated change log

### Security Impact:
- CSP helps prevent XSS attacks by controlling resource loading
- Improved caching reduces server load and improves user experience
- Social media pages now excluded from search engine indexing
