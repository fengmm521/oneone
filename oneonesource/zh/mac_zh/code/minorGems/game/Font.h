#ifndef FONT_INCLUDED
#define FONT_INCLUDED


#include "minorGems/game/gameGraphics.h"
#include "minorGems/util/SimpleVector.h"





#ifdef _WIN32
   //define something for Windows (32-bit and 64-bit, this part is common)
    #include <GL/gl.h>
    #include <GL/glu.h>
    #include <ft2build.h>
    #include <freetype/ftglyph.h>
#elif __APPLE__
    #include "TargetConditionals.h"
    #if TARGET_IPHONE_SIMULATOR
         // iOS Simulator
    #elif TARGET_OS_IPHONE
        // iOS device
    #elif TARGET_OS_MAC
        // Other kinds of Mac OS
        #import <OpenGL/gl.h>
        #import <OpenGL/glu.h>
        #include <ft2build.h>
        #include <freetype/ftglyph.h>

    #else
    #   error "Unknown Apple platform"
    #endif
#elif __ANDROID__
    // android
#elif __linux__
    // linux
#elif __unix__ // all unices not caught above
    // Unix
#elif defined(_POSIX_VERSION)
    // POSIX
#else
#   error "Unknown compiler"
#endif

enum TextAlignment {
    alignCenter = 0,
    alignRight,
    alignLeft 
    };



// a table for a given character
// extra kerning offsets for each character that could follow
// this character
typedef struct KerningTable {
        short offset[256];
    } KerningTable;




struct xCharTexture  
{  
    GLuint  m_texID;  
    wchar_t m_chaID;  
    int     m_Width;  
    int     m_Height;  
  
    int     m_adv_x;  
    int     m_adv_y;  
    int     m_delta_x;  
    int     m_delta_y;  
public:  
    xCharTexture()  
    {  
        m_texID  = 0;  
        m_chaID  = 0;  
        m_Width  = 0;  
        m_Height = 0;  
    }  
};  

class xFreeTypeLib  
{  
    FT_Library m_FT2Lib;  
    FT_Face    m_FT_Face;  
  
public:  
    int   m_w;  
    int   m_h;  
    void load(const char* font_file , int _w , int _h);  
    GLuint loadChar(wchar_t ch);  
};  

class Font {
        
    public:
        
        // file contains TGA with 16x16 ascii table
        // if inFixedCharWidth > 0, it overrides sprite width for width
        // of fixed-spacing characters.
        Font( const char *inFileName, int inCharSpacing, int inSpaceWidth,
              char inFixedWidth,
              double inScaleFactor = 1.0,
              int inFixedCharWidth = 0 );
        
        ~Font();
        

        // copies character spacing and kerning from another font
        // (useful for erased fonts that can't be scanned properly for
        //  spacing but must line up with non-erased version perfectly)
        void copySpacing( Font *inOtherFont );
        
        
        // draws a string on the current screen using set draw color
        // returns x coordinate of string end
        double drawString( const char *inString, doublePair inPosition,
                           TextAlignment inAlign = alignCenter );


        double measureString( const char *inString, int inCharLimit = -1 );
        
        // gets per-character position of string without drawing it
        double getCharPos( SimpleVector<doublePair> *outPositions,
            const char *inString, doublePair inPosition,
            TextAlignment inAlign = alignCenter );
        

        // height of basic, non-accented characters
        double getFontHeight();
        

        // defaults to being on
        void enableKerning( char inKerningOn );


        // sets minimum floating point precision for positioning
        // the start of a string (to avoid round-off errors on graphics
        // cards that don't handle sub-pixel polygon positioning consistently)
        // In most cases, this should be the world dimensions of one
        // screen pixel.
        // Example:  if set to 0.5, the positions of 10.0, 10.5, 11.0
        // are allowed, but 10.35 will be rounded down to 10.0 before the
        // string is drawn.
        // If set to 2, only even positions are allowed, and odd positions
        // are rounded down.
        // Defaults to 0, which indicates no precision limit.
        void setMinimumPositionPrecision( double inMinimum );
        

        double getCharSpacing();
        
        // returns x coordinate to right of drawn character
        double drawCharacter( unsigned char inC, doublePair inPosition );

        // draws sprite centered on inPosition with no spacing adjustments
        void drawCharacterSprite( unsigned char inC, doublePair inPosition );

    private:        
        
        // returns x coordinate to right of drawn character
        double positionCharacter( unsigned char inC, doublePair inTargetPos,
                                  doublePair *outActualPos );

        
        double mScaleFactor;
        
        
        int mCharSpacing;
        int mSpaceWidth;
        
        char mFixedWidth;
        
        int mSpriteWidth;
        int mSpriteHeight;
        
        char mAccentsPresent;
        

        int mCharBlockWidth;
        

        // maps ascii chars to sprite IDs
        SpriteHandle mSpriteMap[ 256 ];
        
        // for kerning (ignored if fixed width flag on)
        int mCharLeftEdgeOffset[ 256 ];
        int mCharWidth[ 256 ];
        
        
        // sparse
        // contains NULL for every blank character
        KerningTable *mKerningTable[256];
        

        char mEnableKerning;

        double mMinimumPositionPrecision;
    };


#endif
