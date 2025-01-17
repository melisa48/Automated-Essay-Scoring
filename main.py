import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import language_tool_python
import statistics

class EssayScorer:
    def __init__(self):
        """Initialize the essay scorer with necessary tools and resources"""
        try:
            resources = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'punkt_tab']
            for resource in resources:
                try:
                    nltk.download(resource, quiet=True)
                except Exception as e:
                    print(f"Warning: Could not download {resource}: {str(e)}")
            
            self.language_tool = language_tool_python.LanguageTool('en-US')
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise
        
    def analyze_essay(self, essay_text):
        try:
            # Basic text preprocessing
            sentences = sent_tokenize(essay_text)
            words = word_tokenize(essay_text)
            words_no_stop = [word.lower() for word in words if word.isalnum() and word.lower() not in self.stop_words]
            
            # Enhanced metrics
            metrics = {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
                'unique_words': len(set(words_no_stop)),
                'vocabulary_richness': len(set(words_no_stop)) / len(words_no_stop) if words_no_stop else 0,
                'paragraph_count': len([s for s in essay_text.split('\n') if s.strip()]),
                'avg_sentence_length': sum(len(word_tokenize(s)) for s in sentences) / len(sentences) if sentences else 0,
                'long_sentences': sum(1 for s in sentences if len(word_tokenize(s)) > 25),
                'short_sentences': sum(1 for s in sentences if len(word_tokenize(s)) < 10)
            }
            
            # Grammar and spelling check
            grammar_errors = self.language_tool.check(essay_text)
            metrics['grammar_error_count'] = len(grammar_errors)
            
            # Sentence structure analysis
            sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences]
            metrics['sentence_length_variation'] = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
            
            # Sentiment and subjectivity analysis
            blob = TextBlob(essay_text)
            metrics['sentiment'] = blob.sentiment.polarity
            metrics['subjectivity'] = blob.sentiment.subjectivity
            
            score = self._calculate_score(metrics)
            feedback = self._generate_feedback(metrics, grammar_errors)
            
            return {
                'score': score,
                'metrics': metrics,
                'feedback': feedback
            }
        except Exception as e:
            print(f"Error during essay analysis: {str(e)}")
            raise
    
    def _calculate_score(self, metrics):
        score = 100
        
        # Enhanced scoring criteria
        if metrics['word_count'] < 300:
            score -= 10
        if metrics['word_count'] < 200:
            score -= 10  # Additional penalty for very short essays
            
        if metrics['avg_words_per_sentence'] > 30:
            score -= 5
        if metrics['avg_words_per_sentence'] < 10:
            score -= 5
            
        if metrics['vocabulary_richness'] < 0.4:
            score -= 10
        if metrics['grammar_error_count'] > 0:
            score -= min(20, metrics['grammar_error_count'] * 2)  # Cap grammar penalty at 20 points
            
        if metrics['long_sentences'] > metrics['sentence_count'] * 0.5:
            score -= 5  # Penalty for too many long sentences
        if metrics['paragraph_count'] < 3 and metrics['word_count'] > 300:
            score -= 5  # Penalty for poor paragraph structure
            
        return max(0, min(100, score))
    
    def _generate_feedback(self, metrics, grammar_errors):
        feedback = []
        
        # Structure feedback
        feedback.append("\nStructure Analysis:")
        if metrics['paragraph_count'] < 3:
            feedback.append("- Consider organizing your essay into more paragraphs for better structure")
        else:
            feedback.append("- Good paragraph structure with clear divisions")
            
        feedback.append(f"- Your essay contains {metrics['paragraph_count']} paragraphs and {metrics['sentence_count']} sentences")
        
        # Length feedback
        feedback.append("\nLength Analysis:")
        if metrics['word_count'] < 300:
            feedback.append("- Essay length is below recommended minimum of 300 words")
            feedback.append(f"- Current word count: {metrics['word_count']} (need {300 - metrics['word_count']} more words)")
        elif metrics['word_count'] > 1000:
            feedback.append("- Essay length is appropriate for detailed analysis")
        
        # Sentence structure feedback
        feedback.append("\nSentence Structure:")
        feedback.append(f"- Average sentence length: {metrics['avg_words_per_sentence']:.1f} words")
        if metrics['long_sentences'] > 0:
            feedback.append(f"- You have {metrics['long_sentences']} long sentences (>25 words)")
        if metrics['short_sentences'] > 0:
            feedback.append(f"- You have {metrics['short_sentences']} short sentences (<10 words)")
        if metrics['sentence_length_variation'] > 10:
            feedback.append("- Good variety in sentence length")
        
        # Vocabulary feedback
        feedback.append("\nVocabulary Usage:")
        feedback.append(f"- You used {metrics['unique_words']} unique words")
        if metrics['vocabulary_richness'] < 0.4:
            feedback.append("- Consider using more varied vocabulary to enhance expression")
        elif metrics['vocabulary_richness'] > 0.6:
            feedback.append("- Excellent vocabulary diversity")
        
        # Grammar feedback
        feedback.append("\nGrammar and Spelling:")
        if grammar_errors:
            feedback.append(f"- Found {len(grammar_errors)} grammar/spelling issues:")
            for error in grammar_errors[:5]:
                feedback.append(f"  * {error.message}")
            if len(grammar_errors) > 5:
                feedback.append(f"  * ({len(grammar_errors) - 5} additional issues not shown)")
        else:
            feedback.append("- No significant grammar or spelling issues found")
        
        # Style and tone feedback
        feedback.append("\nStyle and Tone:")
        if metrics['subjectivity'] > 0.8:
            feedback.append("- The writing style is highly subjective")
        elif metrics['subjectivity'] < 0.2:
            feedback.append("- The writing style is highly objective")
        
        if metrics['sentiment'] > 0.5:
            feedback.append("- The tone is notably positive")
        elif metrics['sentiment'] < -0.5:
            feedback.append("- The tone is notably negative")
        
        return feedback

def main():
    try:
        scorer = EssayScorer()
        
        # Longer sample essay
        sample_essay = """
        The impact of technology on modern education has been transformative and far-reaching, fundamentally changing how students learn and teachers instruct. In the digital age, traditional educational methods have been supplemented and, in some cases, replaced by innovative technological solutions that offer unprecedented opportunities for learning and engagement.

        One of the most significant advantages of technology in education is its ability to provide personalized learning experiences. Through adaptive learning platforms and artificial intelligence, educational content can be tailored to individual student needs, allowing them to learn at their own pace and focus on areas where they need the most help. This personalization has proven particularly beneficial for students who might struggle in traditional classroom settings.

        Furthermore, technology has dramatically improved access to educational resources. Students now have instant access to vast libraries of information, educational videos, interactive simulations, and collaborative tools. This accessibility has democratized education to an extent never before possible, allowing students from diverse backgrounds and geographical locations to access high-quality educational materials.

        However, the integration of technology in education also presents certain challenges that must be carefully addressed. Digital literacy has become a crucial skill, and there is a risk of creating or widening the digital divide between students who have access to technology and those who don't. Teachers must also adapt their teaching methods and develop new skills to effectively utilize these technological tools in their classrooms.

        Despite these challenges, the benefits of technology in education far outweigh the drawbacks. The key lies in thoughtful implementation and ensuring that technology serves as a tool to enhance, rather than replace, the fundamental human elements of education. As we move forward, finding the right balance between traditional teaching methods and technological innovation will be crucial for creating effective and engaging learning environments.
        """
        
        results = scorer.analyze_essay(sample_essay)
        
        print(f"Essay Score: {results['score']}/100\n")
        print("Detailed Metrics:")
        for metric, value in results['metrics'].items():
            print(f"{metric}: {value}")
        print("\nDetailed Feedback:")
        for feedback_item in results['feedback']:
            print(f"{feedback_item}")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print("\nPlease ensure all required packages are installed:")
        print("pip install nltk textblob language-tool-python")

if __name__ == "__main__":
    main()