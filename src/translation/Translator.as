/*
 * Scratch Project Editor and Player
 * Copyright (C) 2014 Massachusetts Institute of Technology
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

package translation {
import blocks.Block;

import flash.events.Event;
import flash.net.*;
import flash.utils.ByteArray;
import flash.utils.Dictionary;

import logging.LogLevel;

import mx.utils.StringUtil;

import uiwidgets.Menu;

import util.*;

public class Translator {

	public static var languages:Array = []; // contains pairs: [<language code>, <utf8 language name>]
	public static var currentLang:String = 'en';

	public static var rightToLeft:Boolean;
	public static var rightToLeftMath:Boolean; // true only for Arabic

	private static const font12:Array = ['fa', 'he','ja','ja_HIRA', 'zh_CN'];
	private static const font13:Array = ['ar'];

	private static var dictionary:Object = {};

	public static function initializeLanguageList():void {
		// Get a list of language names for the languages menu from the server.
		function saveLanguageList(data:String):void {
			if (!data) return;
			for each (var line:String in data.split('\n')) {
				var fields:Array = line.split(',');
				if (fields.length >= 2) {
					languages.push([StringUtil.trim(fields[0]), StringUtil.trim(fields[1])]);
				}
			}
		}
		languages = [['en', 'English'],['se', 'Swedish']]; // English is always the first entry
		Scratch.app.server.getLanguageList(saveLanguageList);
	}

	public static function setLanguageValue(lang:String):void {
		function gotPOFile(data:ByteArray):void {
			if (data) {
				dictionary = parsePOData(data);
				setFontsFor(lang); // also sets currentLang
				checkBlockTranslations();
			}
			Scratch.app.translationChanged();
		}

		dictionary = {}; // default to English (empty dictionary) if there's no .po file
		setFontsFor('en');
		if ('en' == lang) Scratch.app.translationChanged(); // there is no .po file English
		else if ('se' == lang ) {
			var rader:Array = [
													'msgid\"Buttons\"',			'msgstr\"Knappar\"',
													'msgid\"Motion\"',			'msgstr\"Rörelser\"',
													'msgid\"Actions\"',			'msgstr\"Lampor\"',
													'msgid\"Control\"',			'msgstr\"Kontrollera\"',
													'msgid\"Sensing\"',			'msgstr\"Värden\"',
													'msgid\"Operators\"',		'msgstr\"Operatorer\"',
													'msgid\"More Blocks\"',	'msgstr\"Egna block\"',
													'msgid\"When @greenBall clicked\"',				'msgstr\"När @greenBall trycks på\"',
													'msgid\"When @blueBall clicked\"',				'msgstr\"När @blueBall trycks på\"',
													'msgid\"When @yellowBall clicked\"',				'msgstr\"När @yellowBall trycks på\"',
													'msgid\"Increase speed by %n \"',				'msgstr\"öka hastigheten med %n\"',
													'msgid\"Decrease speed by %n \"',				'msgstr\"minska hastigheten med %n\"',
													'msgid\"Forward %n cm\"',			'msgstr\"framåt %n cm\"',
													'msgid\"Backwards %n cm\"',			'msgstr\"backa %n cm\"',
													'msgid\"Max speed\"',			'msgstr\"Maximala hastigheten\"',
													'msgid\"Min speed\"',			'msgstr\"Minimala hastigheten\"',
													'msgid\"turn @turnRight %n degrees\"',			'msgstr\"rotera @turnRight %n grader\"',
													'msgid\"turn @turnLeft %n degrees\"',			'msgstr\"rotera @turnLeft %n grader\"',
													'msgid\"Turn on right LED\"',			'msgstr\"tänd högra LED-lampan\"',
													'msgid\"Turn off right LED\"',			'msgstr\"släck högra LED-lampan\"',
													'msgid\"Turn on left LED\"',			'msgstr\"tänd vänstra LED-lampan\"',
													'msgid\"Turn off left LED\"',			'msgstr\"släck vänstra LED-lampan\"',
													'msgid\"wait %n secs\"',			'msgstr\"vänta %n sekunder\"',
													'msgid\"repeat %n\"',			'msgstr\"upprepa %n gånger\"',
													'msgid\"forever\"',			'msgstr\"upprepa för alltid\"',
													'msgid\"if %b then\"',			'msgstr\"om %b stämmer\"',
													'msgid\"else\"',			'msgstr\"annars\"',
													'msgid\"define\"',			'msgstr\"Definiera\"',
													'msgid\"wait until %b\"',			'msgstr\"vänta tills %b stämmer\"',
													'msgid\"repeat until %b\"',			'msgstr\"upprepa tills %b stämmer\"',
													'msgid\"distance to object \"',			'msgstr\"avstånd till objekt\"',
													'msgid\"timer\"',			'msgstr\"tidtagarurstid\"',
													'msgid\"reset timer\"',			'msgstr\"nollställ tidtagarur\"',
													'msgid\"current %m.timeAndDate\"',			'msgstr\"aktuell %m.timeAndDate\"',
													'msgid\"year\"',			'msgstr\"år\"',
													'msgid\"month\"',			'msgstr\"månad\"',
													'msgid\"date\"',			'msgstr\"dag i månaden\"',
													'msgid\"day of week\"',			'msgstr\"dag i veckan\"',
													'msgid\"hour\"',			'msgstr\"timme\"',
													'msgid\"minute\"',			'msgstr\"minut\"',
													'msgid\"second\"',			'msgstr\"sekund\"',
													'msgid\"pick random %n to %n\"',			'msgstr\"slumptal %n till %n\"',
													'msgid\"%b and %b"\"',			'msgstr\"%b och %b stämmer"\"',
													'msgid\"%b or %b"\"',			'msgstr\"%b eller %b stämmer"\"',
													'msgid\"not %b\"',			'msgstr\"%b stämmer inte\"',
													'msgid\"round %n\"',			'msgstr\"avrunda %n\"',
													'msgid\"%m.mathOp of %n\"',			'msgstr\"%m.mathOp av %n\"',
													'msgid\"set %m.var to %n\"',			'msgstr\"sätt %m.var till %s\"',
													'msgid\"change %m.var by %n\"',			'msgstr\"ändra %m.var med %n\"',
													'msgid\"days since 2000\"',			'msgstr\"dagar sedan milleniumskiftet\"',
													'msgid\"Make a Block\"',			'msgstr\"Skapa ett block\"',
													'msgid\"Make a Variable\"',			'msgstr\"Skapa en variabel\"',
													'msgid\"Make a List\"',			'msgstr\"Skapa en lista\"',
													'msgid\"New Block\"',			'msgstr\"Nytt block\"',
													'msgid\"Options\"',			'msgstr\"Alternativ\"',
													'msgid\"Cancel\"',			'msgstr\"Avbryt\"',
													'msgid\"Add number input:\"',			'msgstr\"Lägg till siffervärde:\"',
													'msgid\"Add boolean input:\\"',			'msgstr\"Lägg till boolskt värde\"',
													'msgid\"Add label text:\\"',			'msgstr\"Lägg till etikettext\"',
													'msgid\"Variable name\"',			'msgstr\"Variabelnamn\"',
													'msgid\"New Variable\"',			'msgstr\"Ny Variabel\"',
													'msgid\"New List\"',			'msgstr\"Ny Lista\"',
													'msgid\"List name\"',			'msgstr\"Listnamn\"',
													'msgid\"File\"',			'msgstr\"Arkiv\"',
													'msgid\"Edit\"',			'msgstr\"Redigera\"',
													'msgid\"New\"',			'msgstr\"Nytt\"',
													'msgid\"Load Project\"',			'msgstr\"Ladda upp från din dator\"',
													'msgid\"Save Project\"',			'msgstr\"Ladda ner till din dator eller usb-minnet för Pedagogo\"',
													'msgid\"Undelete\"',			'msgstr\"Återta\"',
													'msgid\"Edit block colors\"',			'msgstr\"Ändra blockfärger\"',
													'msgid\"Edit Block Colors\"',			'msgstr\"Ändra blockfärger\"',
													'msgid\"duplicate\"',			'msgstr\"Skapa kopia\"',
													'msgid\"Duplicate\"',			'msgstr\"Skapa kopia\"',
													'msgid\"delete\"',			'msgstr\"Ta bort\"',
													'msgid\"Delete\"',			'msgstr\"Ta bort\"',
													'msgid\"Load\"',			'msgstr\"Ladda \"',
													'msgid\"Save\"',			'msgstr\" Spara\"',
													'msgid\"Hue\"',			'msgstr\"Kulör\"',
													'msgid\"Sat.\"',			'msgstr\"Mättnad\"',
													'msgid\"Bri.\"',			'msgstr\"Ljusstyrka\"',
													'msgid\"Apply\"',			'msgstr\"Använd!\"',
													'msgid\"Close\"',			'msgstr\"Stäng\"',
													'msgid\"Category:\"',			'msgstr\"Kategori: \"',
													'msgid\"add %n to %m.list\"',			'msgstr\"lägg till %n i %m.list\"',
													'msgid\"delete %d.listDeleteItem of %m.list\"',			'msgstr\"ta bort %d.listDeleteItem från %m.list\"',
													'msgid\"insert %n at %d.listItem of %m.list\"',			'msgstr\"sätt in %n på %d.listItem i %m.list\"',
													'msgid\"replace item %d.listItem of %m.list with %n\"',			'msgstr\"ersätt %n i %d.listItem med %m.list\"',
													'msgid\"item %d.listItem of %m.list\"',			'msgstr\"objekt %d.listItem i %m.list\"',
													'msgid\"length of %m.list\"',			'msgstr\"längden av %m.list\"',
													'msgid\"%m.list contains %n?\"',			'msgstr\"%m.list innehåller %n?\"',
													'msgid\"xxxx\"',			'msgstr\"xxxxxx\"',
													'msgid\"xxxx\"',			'msgstr\"xxxxxx\"',
													'msgid\"xxxx\"',			'msgstr\"xxxxxx\"',


												];
			dictionary = makeDictionary(rader);
			Scratch.app.translationChanged();
		} else Scratch.app.server.getPOFile(lang, gotPOFile);

	}

	public static function setLanguage(lang:String):void {
		if ('import translation file' == lang) { importTranslationFromFile(); return; }
		if ('set font size' == lang) { fontSizeMenu(); return; }

		setLanguageValue(lang);
		Scratch.app.server.setSelectedLang(lang);
	}

	public static function importTranslationFromFile():void {
		function fileLoaded(e:Event):void {
			var file:FileReference = FileReference(e.target);
			var i:int = file.name.lastIndexOf('.');
			var langName:String = file.name.slice(0, i);
			var data:ByteArray = file.data;
			if (data) {
				dictionary = parsePOData(data);
				setFontsFor(langName);
				checkBlockTranslations();
				Scratch.app.translationChanged();
			}
		}

		Scratch.loadSingleFile(fileLoaded);
	}

	private static function fontSizeMenu():void {
		function setFontSize(labelSize:int):void {
			var argSize:int = Math.round(0.9 * labelSize);
			var vOffset:int = labelSize > 13 ? 1 : 0;
			Block.setFonts(labelSize, argSize, false, vOffset);
			Scratch.app.translationChanged();
		}
		var m:Menu = new Menu(setFontSize);
		for (var i:int = 8; i < 25; i++) m.addItem(i.toString(), i);
		m.showOnStage(Scratch.app.stage);
	}

	private static function setFontsFor(lang:String):void {
		// Set the rightToLeft flag and font sizes the given language.

		currentLang = lang;

		const rtlLanguages:Array = ['ar', 'fa', 'he'];
		rightToLeft = rtlLanguages.indexOf(lang) > -1;
		rightToLeftMath = ('ar' == lang);
		Block.setFonts(10, 9, true, 0); // default font settings
		if (font12.indexOf(lang) > -1) Block.setFonts(11, 10, false, 0);
		if (font13.indexOf(lang) > -1) Block.setFonts(13, 12, false, 0);
	}

	public static function map(s:String, context:Dictionary=null):String {
		var result:* = dictionary[s];
		if ((result == null) || (result.length == 0)) result = s;
		if (context) result = StringUtils.substitute(result, context);
		return result;
	}

	private static function parsePOData(bytes:ByteArray):Object {
		// Parse the given data in gettext .po file format.
		skipBOM(bytes);
		var lines:Array = [];
		while (bytes.bytesAvailable > 0) {
			var s:String = StringUtil.trim(nextLine(bytes));
			if ((s.length > 0) && (s.charAt(0) != '#')) lines.push(s);
		}
		return makeDictionary(lines);
	}

	private static function skipBOM(bytes:ByteArray):void {
		// Some .po files begin with a three-byte UTF-8 Byte Order Mark (BOM).
		// Skip this BOM if it exists, otherwise do nothing.
		if (bytes.bytesAvailable < 3) return;
		var b1:int = bytes.readUnsignedByte();
		var b2:int = bytes.readUnsignedByte();
		var b3:int = bytes.readUnsignedByte();
		if ((b1 == 0xEF) && (b2 == 0xBB) && (b3 == 0xBF)) return; // found BOM
		bytes.position = bytes.position - 3; // BOM not found; back up
	}

	private static function nextLine(bytes:ByteArray):String {
		// Read the next line from the given ByteArray. A line ends with CR, LF, or CR-LF.
		var buf:ByteArray = new ByteArray();
		while (bytes.bytesAvailable > 0) {
			var nextByte:int = bytes.readUnsignedByte();
			if (nextByte == 13) { // CR
				// line could end in CR or CR-LF
				if (bytes.readUnsignedByte() != 10) bytes.position--; // try to read LF, but backup if not LF
				break;
			}
			if (nextByte == 10) break; // LF
			buf.writeByte(nextByte); // append anything else
		}
		buf.position = 0;
		return buf.readUTFBytes(buf.length);
	}

	private static function makeDictionary(lines:Array):Object {
		// Return a dictionary mapping original strings to their translations.
		var dict:Object = {};
		var mode:String = 'none'; // none, key, val
		var key:String = '';
		var val:String = '';
		for each (var line:String in lines) {
			if ((line.length >= 5) && (line.slice(0, 5).toLowerCase() == 'msgid')) {
				if (mode == 'val') dict[key] = val; // recordPairIn(key, val, dict);
				mode = 'key';
				key = '';
			} else if ((line.length >= 6) && (line.slice(0, 6).toLowerCase() == 'msgstr')) {
				mode = 'val';
				val = '';
			}
			if (mode == 'key') key += extractQuotedString(line);
			if (mode == 'val') val += extractQuotedString(line);
		}
		if (mode == 'val') dict[key] = val; // recordPairIn(key, val, dict);
		delete dict['']; // remove the empty-string metadata entry, if present.
		return dict;
	}

	private static function extractQuotedString(s:String):String {
		// Remove leading and trailing whitespace characters.
		var i:int = s.indexOf('"'); // find first double-quote
		if (i < 0) i = s.indexOf(' '); // if no double-quote, start after first space
		var result:String = '';
		for (i = i + 1; i < s.length; i++) {
			var ch:String = s.charAt(i);
			if ((ch == '\\') && (i < (s.length - 1))) {
				ch = s.charAt(++i);
				if (ch == 'n') ch = '\n';
				if (ch == 'r') ch = '\r';
				if (ch == 't') ch = '\t';
			}
			if (ch == '"') return result; // closing double-quote
			result += ch;
		}
		return result;
	}

	private static function checkBlockTranslations():void {
		for each (var entry:Array in Specs.commands) checkBlockSpec(entry[0]);
		for each (var spec:String in Specs.extensionSpecs) checkBlockSpec(spec);
	}

	private static function checkBlockSpec(spec:String):void {
		var translatedSpec:String = map(spec);
		if (translatedSpec == spec) return; // not translated
		if (!argsMatch(extractArgs(spec), extractArgs(translatedSpec))) {
			Scratch.app.log(
					LogLevel.WARNING, 'Block argument mismatch',
					{language: currentLang, spec: spec, translated: translatedSpec});
			delete dictionary[spec]; // remove broken entry from dictionary
		}
	}

	private static function argsMatch(args1:Array, args2:Array):Boolean {
		if (args1.length != args2.length) return false;
		for (var i:int = 0; i < args1.length; i++) {
			if (args1[i] != args2[i]) return false;
		}
		return true;
	}

	private static function extractArgs(spec:String):Array {
		var result:Array = [];
		var tokens:Array = ReadStream.tokenize(spec);
		for each (var s:String in tokens) {
			if ((s.length > 1) && ((s.charAt(0) == '%') || (s.charAt(0) == '@'))) result.push(s);
		}
		return result;
	}

}}
