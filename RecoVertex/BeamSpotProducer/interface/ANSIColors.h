/****************************************************************************
** Authors: Dario Menasce, Stefano Terzo
**
** I.N.F.N. Milan-Bicocca
** Piazza  della Scienza 3, Edificio U2
** Milano, 20126
**
****************************************************************************/

#ifndef _ANSICOLORS_H
#define _ANSICOLORS_H

/*! \file ANSIColors.h
 *  \brief Header file containing macros to highlight output lines with color.
 *
 *  Check also <A HREF="http://www.bluesock.org/~willg/dev/ansi.html">http://www.bluesock.org/~willg/dev/ansi.html</A>
 *
 *  Below is a usage example:
 *  <p><b>
 *  \code
 *   #include <ANSIColors.h>"
 *   ...
 *   cout << ACRed << ACBold << "This text will be highlighted in red" << ACPlain << endl ;
 *  \endcode
 *   </b>
 */

//#define _NOCOLORS_H true

#ifndef _NOCOLORS_H

#define ACBlack       "\e[0;30m"
#define ACBlue        "\e[0;34m"
#define ACGreen       "\e[0;32m"
#define ACCyan        "\e[0;36m"
#define ACRed         "\e[0;31m"
#define ACPurple      "\e[0;35m"
#define ACBrown       "\e[0;33m"
#define ACGray        "\e[0;37m"
#define ACDarkGray    "\e[1;30m"
#define ACLightBlue   "\e[1;34m"
#define ACLightGreen  "\e[1;32m"
#define ACLightCyan   "\e[1;36m"
#define ACLightRed    "\e[1;31m"
#define ACLightPurple "\e[1;35m"
#define ACYellow      "\e[1;33m"
#define ACWhite       "\e[1;37m"

#define ACPlain       "\e[0m"
#define ACBold        "\e[1m"
#define ACUnderline   "\e[4m"
#define ACBlink       "\e[5m"
#define ACReverse     "\e[7m"

#define ACClear       "\e[2J"
#define ACClearL      "\e[2K"

#define ACCR          " \r"

#define ACSave        "\e[s"
#define ACRecall      "\e[u"

#else  // _NOCOLORS_H

#define ACBlack       ""
#define ACBlue        ""
#define ACGreen       ""
#define ACCyan        ""
#define ACRed         ""
#define ACPurple      ""
#define ACBrown       ""
#define ACGray        ""
#define ACDarkGray    ""
#define ACLightBlue   ""
#define ACLightGreen  ""
#define ACLightCyan   ""
#define ACLightRed    ""
#define ACLightPurple ""
#define ACYellow      ""
#define ACWhite       ""

#define ACPlain       ""
#define ACBold        ""
#define ACUnderline   ""
#define ACBlink       ""
#define ACReverse     ""

#define ACClear       ""
#define ACClearL      ""

#define ACCR          ""

#define ACSave        ""
#define ACRecall      ""

#endif // _ANSICOLORS_H

#endif // _ANSICOLORS_H
