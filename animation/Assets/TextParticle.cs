using TMPro;
using UnityEngine;

public class TextParticle : MonoBehaviour
{
    [SerializeField] private float duration = 5f;
    private TextMeshProUGUI textComponent;
    private float elapsedTime = 0f;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        transform.rotation = Quaternion.Euler(0f, 0f, Random.Range(0f, 360f));
        textComponent = GetComponentInChildren<TextMeshProUGUI>();
        Destroy(gameObject, duration);
    }

    // Update is called once per frame
    void Update()
    {
        if (textComponent != null)
        {
            elapsedTime += Time.deltaTime;
            float alpha = Mathf.Lerp(1f, 0f, elapsedTime / duration);
            Color color = textComponent.color;
            color.a = alpha;
            textComponent.color = color;
        }
    }
}