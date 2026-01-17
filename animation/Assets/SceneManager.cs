using System.Collections;
using System.Collections.Generic;
using TMPro;
using Unity.Cinemachine;
using UnityEngine;

public class SceneManager : MonoBehaviour
{
    private static readonly int Typing = Animator.StringToHash("typing");
    private static readonly int Narrating = Animator.StringToHash("narrating");
    private static readonly int Shrink = Animator.StringToHash("shrink");
    private static readonly int Expand = Animator.StringToHash("expand");

    public TextMeshProUGUI typewriterText;
    public TextMeshProUGUI speechBubbleText;
    public GameObject speechBubble;
    public Camera mainCamera;
    public CinemachineCamera cinemachineCamera;

    public GameObject trumpCharacter;
    public GameObject obamaCharacter;

    GameObject character;
    Animator characterAnimator;

    private Queue<string> typeTextQueue = new();
    private bool _isTyping = false;
    public bool IsTyping
    {
        get => _isTyping;
        private set
        {
            _isTyping = value;
            if (characterAnimator != null)
            {
                if (value)
                {
                    cinemachineCamera.Lens.OrthographicSize = 25f;
                    speechBubble.SetActive(false);
                    typewriterText.gameObject.SetActive(true);
                    characterAnimator.SetBool(Narrating, false);
                }
                characterAnimator.SetBool(Typing, value);
            }
        }
    }

    private Queue<string> narrationQueue = new();
    private bool _isNarrating = false;
    public bool IsNarrating
    {
        get => _isNarrating;
        private set
        {
            _isNarrating = value;
            if (characterAnimator != null)
            {
                if (value)
                {
                    cinemachineCamera.Lens.OrthographicSize = 40f;
                    speechBubble.SetActive(true);
                    typewriterText.gameObject.SetActive(false);
                    characterAnimator.SetBool(Typing, false);
                    speechBubble.GetComponent<Animator>().SetTrigger(Expand);
                }
                else
                {
                    speechBubble.GetComponent<Animator>().SetTrigger(Shrink);
                }
                characterAnimator.SetBool(Narrating, value);
            }
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
    
    public void ChangeBackgroundColor(string colorHex)
    {
        mainCamera.backgroundColor = ColorUtility.TryParseHtmlString(colorHex, out Color color) ? color : Color.white;
    }

    IEnumerator typeText(string text)
    {
        const float delay = 0.05f;
        IsTyping = true;
        
        string currentText = "";
        foreach (char c in text)
        {
            currentText += c;
            typewriterText.text = currentText;

            yield return new WaitForSeconds(delay);
        }

        // Check if there's more text in the queue
        if (typeTextQueue.Count > 0)
        {
            StartCoroutine(typeText(typeTextQueue.Dequeue()));
        }

        IsTyping = false;
    }
    
    public void StartTyping(string text)
    {
        if (IsTyping)
        {
            typeTextQueue.Enqueue(text);
        }
        else
        {
            StartCoroutine(typeText(text));
        }
    }

    IEnumerator narrateText(string text)
    {
        const float delay = 0.1f;
        const float longerDelay = 1.9f;
        IsNarrating = true;
        speechBubble.SetActive(true);
        foreach (var line in text.Split('\n'))
        {
            foreach (string word in line.Split(' '))
            {
                speechBubbleText.text += word + " ";
                yield return new WaitForSeconds(delay);
            }
            yield return new WaitForSeconds(longerDelay);
            speechBubbleText.text = "";
        }
        if (narrationQueue.Count > 0)
        {
            StartCoroutine(narrateText(narrationQueue.Dequeue()));
        }
        
        IsNarrating = false;
    }

    public void StartNarration(string narration)
    {
        if (IsNarrating)
        {
            narrationQueue.Enqueue(narration);
        }
        else
        {
            StartCoroutine(narrateText(narration));
        }
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        // Character selection
        // ChangeCharacter("obama");
        // StartTyping("Hello, my name is .\n I am the President of the United States.");
        // StartNarration("Hello, my name is .\nI am the President of the United States.");
    }

    // Update is called once per frame
    void Update()
    {
    }
}