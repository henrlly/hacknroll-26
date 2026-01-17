using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class SceneManager : MonoBehaviour
{
    private static readonly int Typing = Animator.StringToHash("typing");
    private static readonly int Narrating = Animator.StringToHash("narrating");

    public TextMeshProUGUI typewriterText;
    public Camera mainCamera;

    public GameObject trumpCharacter;
    public GameObject obamaCharacter;

    GameObject character;
    Animator characterAnimator;

    private Queue<string> textQueue = new();
    private bool isTyping = false;
    private Queue<string> narrationQueue = new();
    private bool isNarrating = false;

    IEnumerator typeText(string text)
    {
        const float delay = 0.05f;
        isTyping = true;
        characterAnimator.SetBool(Typing, true);
        
        string currentText = "";
        // ... existing code ...
        foreach (char c in text)
        {
            currentText += c;
            typewriterText.text = currentText;

            yield return new WaitForSeconds(delay);
        }

        characterAnimator.SetBool(Typing, false);
        isTyping = false;

        // Check if there's more text in the queue
        if (textQueue.Count > 0)
        {
            StartCoroutine(typeText(textQueue.Dequeue()));
        }
    }
    
    public void ChangeBackgroundColor(string colorHex)
    {
        mainCamera.backgroundColor = ColorUtility.TryParseHtmlString(colorHex, out Color color) ? color : Color.white;
    }

    public void StartTyping(string text)
    {
        if (isTyping)
        {
            textQueue.Enqueue(text);
        }
        else
        {
            StartCoroutine(typeText(text));
        }
    }

    public void ChangeCharacter(string characterName)
    {
        if (character != null)
        {
            Destroy(character);
        }
        switch (characterName)
        {
            case "trump":
                character = Instantiate(trumpCharacter, new Vector3(0, -28, 0), Quaternion.identity);
                break;
            case "obama":
                character = Instantiate(obamaCharacter, new Vector3(0, -28, 0), Quaternion.identity);
                break;
        }
        characterAnimator = character.GetComponent<Animator>();
    }

    IEnumerator narrateText(string text)
    {
        const float delay = 0.05f;
        isNarrating = true;
        characterAnimator.SetBool(Narrating, true);
        yield return new WaitForSeconds(4f);
        characterAnimator.SetBool(Narrating, false);
        isNarrating = false;
    }

    public void StartNarration(string narration)
    {
        
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        // Character selection
        ChangeCharacter("obama");
    }

    // Update is called once per frame
    void Update()
    {
    }
}