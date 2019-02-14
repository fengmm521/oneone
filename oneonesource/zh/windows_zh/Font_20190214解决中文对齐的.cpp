#include "Font.h"

#include "minorGems/graphics/RGBAImage.h"

#include <string.h>
#include <windows.h>


typedef union rgbaColor {
        struct comp { 
                unsigned char r;
                unsigned char g;
                unsigned char b;
                unsigned char a;
            } comp;
        
        // access those bytes as an array
        unsigned char bytes[4];
        
        // reinterpret those bytes as an unsigned int
        unsigned int rgbaInt; 
    } rgbaColor;


// what alpha level counts as "ink" when measuring character width
// and doing kerning
// values at or below this level will not count as ink
// this improves kerning and font spacing, because dim "tips" of pointed
// glyphs don't cause the glyph to be logically wider than it looks visually 
const unsigned char inkA = 127;

void xFreeTypeLib::load(const char* font_file , int _w , int _h)  
{  
    FT_Library library;  
    if (FT_Init_FreeType( &library) )   
        exit(0);  
    //加载一个字体,取默认的Face,一般为Regualer  
    if (FT_New_Face( library, font_file, 0, &m_FT_Face ))   
        exit(0);  
    //选择字符表  
    FT_Select_Charmap(m_FT_Face, FT_ENCODING_UNICODE);  
    m_w = _w ; m_h = _h;  
    m_FT_Face->num_fixed_sizes;  
    //大小要乘64.这是规定。照做就可以了。  
    // FT_Set_Char_Size( m_FT_Face , 0 , m_w << 6, 96, 96);  
    //用来存放指定字符宽度和高度的特定数据  
    FT_Set_Pixel_Sizes(m_FT_Face,m_w, m_h);  
}  

GLuint xFreeTypeLib::loadChar(wchar_t ch)  
{  
	//if(true) return 1;
    if(mCharTexure[ch].m_texID)  
		return mCharTexure[ch].m_texID;  
    /* 装载字形图像到字形槽（将会抹掉先前的字形图像） */   
    if(FT_Load_Char(m_FT_Face, ch, /*FT_LOAD_RENDER|*/FT_LOAD_FORCE_AUTOHINT|  
        (TRUE ? FT_LOAD_TARGET_NORMAL : FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO) )   )  
    {  
        return 0;  
    }  

    xCharTexture& charTex = mCharTexure[ch];  

    //得到字模  
    FT_Glyph glyph;  
    //把字形图像从字形槽复制到新的FT_Glyph对象glyph中。这个函数返回一个错误码并且设置glyph。   
    if(FT_Get_Glyph( m_FT_Face->glyph, &glyph ))  
        return 0;  

    //转化成位图  
    FT_Render_Glyph( m_FT_Face->glyph,   FT_RENDER_MODE_LCD );//FT_RENDER_MODE_NORMAL  );   
    FT_Glyph_To_Bitmap( &glyph, ft_render_mode_normal, 0, 1 );  
    FT_BitmapGlyph bitmap_glyph = (FT_BitmapGlyph)glyph;  

    //取道位图数据  
    FT_Bitmap& bitmap=bitmap_glyph->bitmap;  

    //把位图数据拷贝自己定义的数据区里.这样旧可以画到需要的东西上面了。  
    int width  =  bitmap.width;  
    int height =  bitmap.rows;  

    m_FT_Face->size->metrics.y_ppem;      //伸缩距离到设备空间  
    m_FT_Face->glyph->metrics.horiAdvance;  //水平文本排列  


    charTex.m_Width = width;  
    charTex.m_Height = height;  
    charTex.m_adv_x = m_FT_Face->glyph->advance.x / 64.0f;  //步进宽度  
    charTex.m_adv_y = m_FT_Face->size->metrics.y_ppem;        //m_FT_Face->glyph->metrics.horiBearingY / 64.0f;  
    charTex.m_delta_x = (float)bitmap_glyph->left;           //left:字形原点(0,0)到字形位图最左边象素的水平距离.它以整数象素的形式表示。   
    charTex.m_delta_y = (float)bitmap_glyph->top - height;   //Top: 类似于字形槽的bitmap_top字段。 
	//charTex.m_texID = 1;	
    glGenTextures(1,&charTex.m_texID);  
    glBindTexture(GL_TEXTURE_2D,charTex.m_texID);  
    char* pBuf = new char[width * height * 4];  
    for(int j=0; j  < height ; j++)  
    {  
        for(int i=0; i < width; i++)  
        {  
            unsigned char _vl =  (i>=bitmap.width || j>=bitmap.rows) ? 0 : bitmap.buffer[i + bitmap.width*j];  
            pBuf[(4*i + (height - j - 1) * width * 4)  ] = 0xFF;  
            pBuf[(4*i + (height - j - 1) * width * 4)+1] = 0xFF;  
            pBuf[(4*i + (height - j - 1) * width * 4)+2] = 0xFF;  
            pBuf[(4*i + (height - j - 1) * width * 4)+3] = _vl;  
        }  
     }  

    glTexImage2D( GL_TEXTURE_2D,0,GL_RGBA,width, height,0,GL_RGBA,GL_UNSIGNED_BYTE,pBuf);  //指定一个二维的纹理图片  
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP);                            //glTexParameteri():纹理过滤  
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP);  
    glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );  
    glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );  
    glTexEnvi(GL_TEXTURE_2D,GL_TEXTURE_ENV_MODE,GL_REPLACE);                                //纹理进行混合  
	delete[] pBuf; 

    /*gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE, pBuf); 
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP); 
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP); 
    glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST ); 
    glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST ); 
    glTexEnvi(GL_TEXTURE_2D,GL_TEXTURE_ENV_MODE,GL_REPLACE);*/  
     
	return charTex.m_texID;
    //return charTex.m_chaID;  
}  


// xFreeTypeLib g_FreeTypeLib;

wchar_t* AnsiToUnicode(const char* lpcstr) 
{   
    wchar_t* Pwstr;  
    int i;  
    i = MultiByteToWideChar(CP_ACP,0,lpcstr,-1,NULL,0);  
    Pwstr = new wchar_t[i];
    MultiByteToWideChar(CP_ACP,0,lpcstr,-1,Pwstr,i);  

    return (Pwstr);  
}  

xCharTexture* Font::getCharTexture(wchar_t ch)  
{  
    mFreeTypeLib.loadChar(ch);  
    return &mFreeTypeLib.mCharTexure[ch];
}  

void Font::drawText(wchar_t* _strText,int x , int y, int maxW , int h, TextAlignment align)  
{
    int maxH = h;  
    size_t nLen = wcslen(_strText);  

    int i;
	// total width of the string
    int tw = 0;
    for(i = 0 ; i <nLen; i ++)  
    {
        if(_strText[i] =='\n')  
        {  
            continue;  
        }  
        xCharTexture* pCharTex = getCharTexture(_strText[i]);  
        // tw += pCharTex->m_Width;
        tw += pCharTex->m_delta_x;
        tw += pCharTex->m_adv_x;
    }

	// align the text horizontally
    if(align == alignCenter)
        x -= tw / 2;

    if(align == alignRight)
        x -= tw;

	// align to center vertically
    ///y += h / 2;

    int sx = x;  
    int sy = y;  
	
	int offsetY = - measureStringHeight(_strText) / 2;
	offsetY = - h / 2 * 0;

    for(i = 0 ; i <nLen ; i ++)  
    {  
        if(_strText[i] =='\n')  
        {  
            sx = x ; sy += maxH + 16;  
            continue;  
        }  
        xCharTexture* pCharTex = getCharTexture(_strText[i]);
		//glEnable( GL_TEXTURE_2D );// 启用2D纹理
        glBindTexture(GL_TEXTURE_2D,pCharTex->m_texID);                          //绑定到目标纹理  
        //glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );     
        //glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );  
        //glEnable(GL_BLEND);                                                     //打开或关闭OpenGL的特殊功能  
        //glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);                       //特殊的像素算法  
        //glDisable(GL_TEXTURE_2D);  
		//glDisable(GL_BLEND);
        int w = pCharTex->m_Width;  
        int h = pCharTex->m_Height;  

        int ch_x = sx + pCharTex->m_delta_x;  
        int ch_y = sy + offsetY + pCharTex->m_delta_y;  
		//if(true)return;
        if(maxH < h) maxH = h;  
        glBegin ( GL_QUADS );                                                    // 定义一个或一组原始的顶点  
        {  
			//倒置文字
            // glTexCoord2f(0.0f, 1.0f); glVertex3f(ch_x      , ch_y    ,  1.0f);  
            // glTexCoord2f(1.0f, 1.0f); glVertex3f(ch_x +  w, ch_y    ,  1.0f);  
            // glTexCoord2f(1.0f, 0.0f); glVertex3f(ch_x +  w, ch_y + h,  1.0f);  
            // glTexCoord2f(0.0f, 0.0f); glVertex3f(ch_x     , ch_y + h,  1.0f);  

			//正向文字
            glTexCoord2f(0.0f, 1.0f); glVertex3f(ch_x      , ch_y + h    ,  1.0f);  
            glTexCoord2f(1.0f, 1.0f); glVertex3f(ch_x +  w, ch_y + h   ,  1.0f);  
            glTexCoord2f(1.0f, 0.0f); glVertex3f(ch_x +  w, ch_y,  1.0f);  
            glTexCoord2f(0.0f, 0.0f); glVertex3f(ch_x     , ch_y,  1.0f);  
        }  
        glEnd();  
        sx += pCharTex->m_adv_x;  
        if(sx > x + maxW)  
        {  
            sx = x ; sy += maxH + 16;  
        }  
    }  
}  


Font::Font( const char *inFileName, int inCharSpacing, int inSpaceWidth,
            char inFixedWidth, double inScaleFactor, int inFixedCharWidth )
        : mScaleFactor( inScaleFactor ),
          mCharSpacing( inCharSpacing ), mSpaceWidth( inSpaceWidth ),
          mFixedWidth( inFixedWidth ), mEnableKerning( true ),
          mMinimumPositionPrecision( 0 ) {

    mFreeTypeLib.load("font.ttf", (int)inScaleFactor, (int)inScaleFactor);
		  
    for( int i=0; i<256; i++ ) {
        mSpriteMap[i] = NULL;
        mKerningTable[i] = NULL;
        }
    


    Image *spriteImage = readTGAFile( inFileName );
    
    if( spriteImage != NULL ) {
        
        int width = spriteImage->getWidth();
        
        int height = spriteImage->getHeight();
        
        int numPixels = width * height;
        
        rgbaColor *spriteRGBA = new rgbaColor[ numPixels ];
        
        
        unsigned char *spriteBytes = 
            RGBAImage::getRGBABytes( spriteImage );
        
        delete spriteImage;

        for( int i=0; i<numPixels; i++ ) {
            
            for( int b=0; b<4; b++ ) {
                
                spriteRGBA[i].bytes[b] = spriteBytes[ i*4 + b ];
                }
            }
        
        delete [] spriteBytes;
        
        

        // use red channel intensity as transparency
        // make entire image solid white and use transparency to 
        // mask it

        for( int i=0; i<numPixels; i++ ) {
            spriteRGBA[i].comp.a = spriteRGBA[i].comp.r;
            
            spriteRGBA[i].comp.r = 255;
            spriteRGBA[i].comp.g = 255;
            spriteRGBA[i].comp.b = 255;
            }
            
                        
                
        mSpriteWidth = width / 16;
        mSpriteHeight = height / 16;
        
        if( mSpriteHeight == mSpriteWidth ) {
            mAccentsPresent = false;
            }
        else {
            mAccentsPresent = true;
            }

        if( inFixedCharWidth == 0 ) {
            mCharBlockWidth = mSpriteWidth;
            }
        else {
            mCharBlockWidth = inFixedCharWidth;
            }


        int pixelsPerChar = mSpriteWidth * mSpriteHeight;
            
        // hold onto these for true kerning after
        // we've read this data for all characters
        rgbaColor *savedCharacterRGBA[256];
        

        for( int i=0; i<256; i++ ) {
            int yOffset = ( i / 16 ) * mSpriteHeight;
            int xOffset = ( i % 16 ) * mSpriteWidth;
            
            rgbaColor *charRGBA = new rgbaColor[ pixelsPerChar ];
            
            for( int y=0; y<mSpriteHeight; y++ ) {
                for( int x=0; x<mSpriteWidth; x++ ) {
                    
                    int imageIndex = (y + yOffset) * width
                        + x + xOffset;
                    int charIndex = y * mSpriteWidth + x;
                    
                    charRGBA[ charIndex ] = spriteRGBA[ imageIndex ];
                    }
                }
                
            // don't bother consuming texture ram for blank sprites
            char allTransparent = true;
            
            for( int p=0; p<pixelsPerChar && allTransparent; p++ ) {
                if( charRGBA[ p ].comp.a != 0 ) {
                    allTransparent = false;
                    }
                }
                
            if( !allTransparent ) {
                
                // convert into an image
                Image *charImage = new Image( mSpriteWidth, mSpriteHeight,
                                              4, false );
                
                for( int c=0; c<4; c++ ) {
                    double *chan = charImage->getChannel(c);
                    
                    for( int p=0; p<pixelsPerChar; p++ ) {
                        
                        chan[p] = charRGBA[p].bytes[c] / 255.0;
                        }
                    }
                

                mSpriteMap[i] = 
                    fillSprite( charImage );
                delete charImage;
                }
            else {
                mSpriteMap[i] = NULL;
                }
            

            if( mFixedWidth ) {
                mCharLeftEdgeOffset[i] = 0;
                mCharWidth[i] = mCharBlockWidth;
                }
            else if( allTransparent ) {
                mCharLeftEdgeOffset[i] = 0;
                mCharWidth[i] = mSpriteWidth;
                }
            else {
                // implement pseudo-kerning
                
                int farthestLeft = mSpriteWidth;
                int farthestRight = 0;
                
                char someInk = false;
                
                for( int y=0; y<mSpriteHeight; y++ ) {
                    for( int x=0; x<mSpriteWidth; x++ ) {
                        
                        unsigned char a = 
                            charRGBA[ y * mSpriteWidth + x ].comp.a;
                        
                        if( a > inkA ) {
                            someInk = true;
                            
                            if( x < farthestLeft ) {
                                farthestLeft = x;
                                }
                            if( x > farthestRight ) {
                                farthestRight = x;
                                }
                            }
                        }
                    }
                
                if( ! someInk  ) {
                    mCharLeftEdgeOffset[i] = 0;
                    mCharWidth[i] = mSpriteWidth;
                    }
                else {
                    mCharLeftEdgeOffset[i] = farthestLeft;
                    mCharWidth[i] = farthestRight - farthestLeft + 1;
                    }
                }
                

            if( !allTransparent && ! mFixedWidth ) {
                savedCharacterRGBA[i] = charRGBA;
                }
            else {
                savedCharacterRGBA[i] = NULL;
                delete [] charRGBA;
                }
            }
        

        // now that we've read in all characters, we can do real kerning
        if( !mFixedWidth )
        for( int i=0; i<256; i++ ) {
            if( savedCharacterRGBA[i] != NULL ) {
                
                mKerningTable[i] = new KerningTable;


                // for each character that could come after this character
                for( int j=0; j<256; j++ ) {

                    mKerningTable[i]->offset[j] = 0;

                    // not a blank character
                    if( savedCharacterRGBA[j] != NULL ) {
                        
                        short minDistance = 2 * mSpriteWidth;

                        // for each pixel row, find distance
                        // between the right extreme of the first character
                        // and the left extreme of the second
                        for( int y=0; y<mSpriteHeight; y++ ) {
                            
                            int rightExtreme = 0;
                            int leftExtreme = mSpriteWidth;
                            
                            for( int x=0; x<mSpriteWidth; x++ ) {
                                int p = y * mSpriteWidth + x;
                                
                                if( savedCharacterRGBA[i][p].comp.a > inkA ) {
                                    rightExtreme = x;
                                    }
                                if( x < leftExtreme &&
                                    savedCharacterRGBA[j][p].comp.a > inkA ) {
                                    
                                    leftExtreme = x;
                                    }
                                // also check pixel rows above and below
                                // for left character, to look for
                                // diagonal collisions (perfect nesting
                                // with no vertical gap)
                                if( y > 0 && x < leftExtreme ) {
                                    int pp = (y-1) * mSpriteWidth + x;
                                    if( savedCharacterRGBA[j][pp].comp.a 
                                        > inkA ) {
                                    
                                        leftExtreme = x;
                                        }
                                    }
                                if( y < mSpriteHeight - 1 
                                    && x < leftExtreme ) {
                                    
                                    int pp = (y+1) * mSpriteWidth + x;
                                    if( savedCharacterRGBA[j][pp].comp.a 
                                        > inkA ) {
                                    
                                        leftExtreme = x;
                                        }
                                    }
                                }
                            
                            int rowDistance =
                                ( mSpriteWidth - rightExtreme - 1 ) 
                                + leftExtreme;

                            if( rowDistance < minDistance ) {
                                minDistance = rowDistance;
                                }
                            }
                        
                        // have min distance across all rows for 
                        // this character pair

                        // of course, we've already done pseudo-kerning
                        // based on character width, so take that into account
                        // true kerning is a tweak to that
                        
                        // pseudo-kerning already accounts for
                        // gap to left of second character
                        minDistance -= mCharLeftEdgeOffset[j];
                        // pseudo-kerning already accounts for gap to right
                        // of first character
                        minDistance -= 
                            mSpriteWidth - 
                            ( mCharLeftEdgeOffset[i] + mCharWidth[i] );
                        
                        if( minDistance > 0 
                            // make sure we don't have a full overhang
                            // for characters that don't collide horizontally
                            // at all
                            && minDistance < mCharWidth[i] ) {
                            
                            mKerningTable[i]->offset[j] = - minDistance;
                            }
                        }
                    }
                
                }
            }
        

        for( int i=0; i<256; i++ ) {
            if( savedCharacterRGBA[i] != NULL ) {
                delete [] savedCharacterRGBA[i];
                }
            }
        

        delete [] spriteRGBA;
        }
    }



Font::~Font() {
    for( int i=0; i<256; i++ ) {
        if( mSpriteMap[i] != NULL ) {
            freeSprite( mSpriteMap[i] );
            }
        if( mKerningTable[i] != NULL ) {
            delete mKerningTable[i];
            }
        }
    }



void Font::copySpacing( Font *inOtherFont ) {
    memcpy( mCharLeftEdgeOffset, inOtherFont->mCharLeftEdgeOffset,
            256 * sizeof( int ) );

    memcpy( mCharWidth, inOtherFont->mCharWidth,
            256 * sizeof( int ) );
    

    for( int i=0; i<256; i++ ) {
        if( mKerningTable[i] != NULL ) {
            delete mKerningTable[i];
            mKerningTable[i] = NULL;
            }

        if( inOtherFont->mKerningTable[i] != NULL ) {
            mKerningTable[i] = new KerningTable;
            memcpy( mKerningTable[i]->offset,
                    inOtherFont->mKerningTable[i]->offset,
                    256 * sizeof( short ) );
            }
        }

    mScaleFactor = inOtherFont->mScaleFactor;
        
    
    mCharSpacing = inOtherFont->mCharSpacing;
    mSpaceWidth = inOtherFont->mSpaceWidth;
        
    mFixedWidth = inOtherFont->mFixedWidth;
        
    mSpriteWidth = inOtherFont->mSpriteWidth;
    mSpriteHeight = inOtherFont->mSpriteHeight;
    
    mAccentsPresent = inOtherFont->mAccentsPresent;
        

    mCharBlockWidth = inOtherFont->mCharBlockWidth;
    }



// double pixel size
static double scaleFactor = 1.0 / 16;
//static double scaleFactor = 1.0 / 8;



double Font::getCharSpacing() {
    double scale = scaleFactor * mScaleFactor;
    
    return mCharSpacing * scale;
    }



double Font::getCharPos( SimpleVector<doublePair> *outPositions,
                         const char *inString, doublePair inPosition,
                         TextAlignment inAlign ) {

    double scale = scaleFactor * mScaleFactor;
    
    unsigned int numChars = strlen( inString );
    
    double x = inPosition.x;
    
    
    double y = inPosition.y;

    // compensate for extra headspace in accent-equipped font files
    if( mAccentsPresent ) { 
        y += scale * mSpriteHeight / 4;
        }

    
    double stringWidth = 0;
    
    if( inAlign != alignLeft ) {
        stringWidth = measureString( inString );
        }
    
    switch( inAlign ) {
        case alignCenter:
            x -= stringWidth / 2;
            break;
        case alignRight:
            x -= stringWidth;
            break;
        default:
            // left?  do nothing
            break;            
        }
    
    // character sprites are drawn on their centers, so the alignment
    // adjustments above aren't quite right.
    x += scale * mSpriteWidth / 2;


    if( mMinimumPositionPrecision > 0 ) {
        x /= mMinimumPositionPrecision;
        
        x = lrint( floor( x ) );
        
        x *= mMinimumPositionPrecision;
        }
    

    for( unsigned int i=0; i<numChars; i++ ) {
        doublePair charPos = { x, y };
        
        doublePair drawPos;
        
        double charWidth = positionCharacter( (unsigned char)( inString[i] ), 
                                              charPos, &drawPos );
        outPositions->push_back( drawPos );
        
        x += charWidth + mCharSpacing * scale;
        
        if( !mFixedWidth && mEnableKerning 
            && i < numChars - 1 
            && mKerningTable[(unsigned char)( inString[i] )] != NULL ) {
            // there's another character after this
            // apply true kerning adjustment to the pair
            int offset = mKerningTable[ (unsigned char)( inString[i] ) ]->
                offset[ (unsigned char)( inString[i+1] ) ];
            x += offset * scale;
            }
        }
    // no spacing after last character
    x -= mCharSpacing * scale;

    return x;
    }




double Font::drawString( const char *inString, doublePair inPosition,
                         TextAlignment inAlign ) {
	glEnable ( GL_TEXTURE_2D );  
	wchar_t *wstr = AnsiToUnicode(inString);  
	drawText(wstr, inPosition.x, inPosition.y, 2048, mScaleFactor, inAlign);
	delete[] wstr;
	return 0;
							 /**
    SimpleVector<doublePair> pos( strlen( inString ) );

    double returnVal = getCharPos( &pos, inString, inPosition, inAlign );

    double scale = scaleFactor * mScaleFactor;
    
    for( int i=0; i<pos.size(); i++ ) {
        SpriteHandle spriteID = mSpriteMap[ (unsigned char)( inString[i] ) ];
    
        if( spriteID != NULL ) {
            drawSprite( spriteID, pos.getElementDirect(i), scale );
            }
    
        }
    
    return returnVal;
	**/
    }




double Font::positionCharacter( unsigned char inC, doublePair inTargetPos,
                                doublePair *outActualPos ) {
    *outActualPos = inTargetPos;
    
    double scale = scaleFactor * mScaleFactor;

    if( inC == ' ' ) {
        return mSpaceWidth * scale;
        }

    if( !mFixedWidth ) {
        outActualPos->x -= mCharLeftEdgeOffset[ inC ] * scale;
        }
    
    if( mFixedWidth ) {
        return mCharBlockWidth * scale;
        }
    else {
        return mCharWidth[ inC ] * scale;
        }
    }

    


double Font::drawCharacter( unsigned char inC, doublePair inPosition ) {
    
    doublePair drawPos;
    double returnVal = positionCharacter( inC, inPosition, &drawPos );

    if( inC == ' ' ) {
        return returnVal;
        }

    SpriteHandle spriteID = mSpriteMap[ inC ];
    
    if( spriteID != NULL ) {
        double scale = scaleFactor * mScaleFactor;
        drawSprite( spriteID, drawPos, scale );
        }
    
    return returnVal;
    }



void Font::drawCharacterSprite( unsigned char inC, doublePair inPosition ) {
    SpriteHandle spriteID = mSpriteMap[ inC ];
    
    if( spriteID != NULL ) {
        double scale = scaleFactor * mScaleFactor;
        drawSprite( spriteID, inPosition, scale );
        }
    }

int Font::measureStringHeight(wchar_t* wstr) {
	int numChars = 9999;
	int height = 0;

	size_t nLen = wcslen(wstr);  

    int i;
    for(i = 0 ; i <nLen && i < numChars; i ++)  
    {
        xCharTexture* pCharTex = getCharTexture(wstr[i]);
        int h = pCharTex->m_Height;
		if(height < h) height = h;
    }

	delete[] wstr;
	return height;
}
	

double Font::measureString( const char *inString, int inCharLimit ) {
	int numChars = 99999;//inCharLimit;
	double width = 0;

	wchar_t *wstr = AnsiToUnicode(inString);  

	size_t nLen = wcslen(wstr);  

    int i;
    for(i = 0 ; i <nLen && i < numChars; i ++)  
    {
        xCharTexture* pCharTex = getCharTexture(wstr[i]); 
		// width += pCharTex->m_Width;		
        width += pCharTex->m_delta_x;
        width += pCharTex->m_adv_x;
    }

	delete[] wstr;
	return width;
	/**
    double scale = scaleFactor * mScaleFactor;

    int numChars = inCharLimit;

    if( numChars == -1 ) {
        // no limit, measure whole string
        numChars = strlen( inString );
        }
    
    double width = 0;
    
    for( int i=0; i<numChars; i++ ) {
        unsigned char c = inString[i];
        
        if( c == ' ' ) {
            width += mSpaceWidth * scale;
            }
        else if( mFixedWidth ) {
            width += mCharBlockWidth * scale;
            }
        else {
            width += mCharWidth[ c ] * scale;

            if( mEnableKerning
                && i < numChars - 1 
                && mKerningTable[(unsigned char)( inString[i] )] != NULL ) {
                // there's another character after this
                // apply true kerning adjustment to the pair
                int offset = mKerningTable[ (unsigned char)( inString[i] ) ]->
                    offset[ (unsigned char)( inString[i+1] ) ];
                width += offset * scale;
                }
            }
    
        width += mCharSpacing * scale;
        }

    if( numChars > 0 ) {    
        // no extra space at end
        // (added in last step of loop)
        width -= mCharSpacing * scale;
        }
    
    return width;
	**/
    }



double Font::getFontHeight() {
	return mScaleFactor;
	/**
    double accentFactor = 1.0f;
    
    if( mAccentsPresent ) {
        accentFactor = 0.5f;
        }
    
    return scaleFactor * mScaleFactor * mSpriteHeight * accentFactor;
	**/
    }



void Font::enableKerning( char inKerningOn ) {
    mEnableKerning = inKerningOn;
    }



void Font::setMinimumPositionPrecision( double inMinimum ) {
    mMinimumPositionPrecision = inMinimum;
    }



